debug = 0

class Event:
    src = None
    eventType = None
    dests = None
    CPUCycles = None
    messageSize = None
    RXDependencies = None
    TXDependency = None
    def __init__( self, node0, eventType, node1, CPUCycles, messageSize, RXDependencies = None, TXDependency = None ):
        self.src = int( node0 ) if eventType == 'P' else int( node1 )
        self.eventType = eventType
        self.dest = [ int( node1 ) ] if eventType == 'P' else [ int( node0 ) ]
        self.CPUCycles = int( CPUCycles )
        self.messageSize = int( messageSize )
        self.RXDependencies = RXDependencies
        self.TXDependency = TXDependency

    def srcDestPair( self ):
        return ( self.src, self.dest )

    def __str__( self ):
        return "%d %s %d %d %d %s %d\n" % ( self.src, self.eventType, str( self.dest ), self.CPUCycles, self.messageSize, str( self.RXDependencies ), self.TXDependency )

def outputEvent( event ):
    if event.eventType in [ 'produce', 'P' ]:
        numFlitsRemaining = math.ceil( event.messageSize / flitSize )
        while numFlitsRemaining > 1:
            numFlitsThisPacket = maxFlitsInPacket if numFlitsRemaining >= maxFlitsInPacket else numFlitsRemaining

            #Output head flit
            numFlitsRemaining -= 1
            outputFlit( 'H', event )

            #Output body flits
            for i in range( 0, numFlitsThisPacket - 2 ): #Offset of two to allow for head and tail flits
                numFlitsRemaining -= 1
                outputFlit( flitType = "B" )

            #Output tail flit
            numFlitsRemaining -= 1
            outputFlit( 'T', event )

        #If packet consists of single flit, output 'S'-type flit
        if numFlitsRemaining == 1:
            numFlitsRemaining -= 1
            outputFlit( 'S', event )

def outputFlit( flitType, event ):
    #Only the first flit needs to carry RX and TX dependency information. Subsequent flits only need a TX dependency on the previous flit.
    TXDependency = event.TXDependency if totalNumFlits == event.first else totalNumFlits - 1
    RXDependencies = event.RXDependencies if totalNumFlits == event.first else []

    #Assemble line from event information and convert to string
    line = [ event.src, flitType, len( event.dests ) ] + event.dests + [ event.data, event.CPUCycles, len( RXDependencies ), TXDependency ] + RXDependencies + [ '\n' ]
    lineAsStrList = [ str( value ) for value in line ]
    lineAsStr = ' '.join( lineAsStrList )
    if debug > 0:
        print lineAsStr
    outFile.write( lineAsStr )


