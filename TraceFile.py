debug = 0

from Event import *

class TraceFile:
    traceFilename = None
    traceFilePosition = None
    blockedOnEvent = None
    complete = None
    eventNumber = None
    registeredEvents = None
    def __init__( self, traceFilename ):
        self.traceFilename = traceFilename
        self.traceFilePosition = 0
        self.blockedOnEvent = None
        self.complete = False
        self.eventNumber = 0
        self.registeredEvents = 0

    def __str__( self ):
        return self.traceFilename

    def ready( self ):
        return not self.complete and ( self.blockedOnEvent is None or registerEvent( self, self.blockedOnEvent ) )

def getReadyFiles( traceFiles ):
    readyFiles = []
    for traceFile in traceFiles:
        if traceFile.ready():
            traceFile.blockedOnEvent = None
            readyFiles.append( traceFile )
    return readyFiles

def readReadyFiles( readyFiles = None ):
    if readyFiles is None:
        readyFiles = getReadyFiles()
    for traceFile in readyFiles:
        if debug > 0:
            print "opening trace file: %s" % traceFile.traceFilename
        with open( traceFile.traceFilename, "rb" ) as dataFile:
            dataFile.seek( traceFile.traceFilePosition, 0 )
            while True:
                line = dataFile.readline()
                if line == '':
                    break
                if debug > 0:
                    print line,
                try:
                    event = Event( *line.split() )
                except TypeError:
                    if debug > 0:
                        print line.split()
                    sys.exit(1)
                traceFile.eventNumber += 1
                if not registerEvent( traceFile, event ): #if event is a blocking consume:
                    traceFile.traceFilePosition = dataFile.tell() #record current position of file
                    if debug > 0:
                        print "Position: %d" % dataFile.tell()
                    traceFile.blockedOnEvent = event #record blocking consume
                    break
            if traceFile.blockedOnEvent is None:
                traceFile.complete = True

def registerEvent( traceFile, event ):
    if event.eventType in [ 'produce', 'P' ]:
        if event.srcDestPair() in eventCounter:
            eventCounter[ event.srcDestPair() ] += 1
        else:
            eventCounter[ event.srcDestPair() ] = 1
    else:
        if event.srcDestPair() in eventCounter and eventCounter[ event.srcDestPair() ] > 0:
            eventCounter[ event.srcDestPair() ] -= 1
        else:
            if debug > 0:
                print "Blocked on event: %s" % str( event )
            return False
    if debug > 0:
        print "Registering event: %s" % str( event )
    outputEvent( event )
    traceFile.registeredEvents += 1
    return True
