#!/home/mkelner/.ENV/bin/python

import sys, os, glob, math
from Event import *
from Trace import *

debug = 0
totalNumFlits = 0
packetSize = None
flitSize = None
eventCounter = {}
outFilename = 'all.trace'
outFile = open( outFilename, "w" )
traceFilenames = glob.glob( '*.trace' )
if outFilename in traceFilenames:
    traceFilenames.remove( outFilename )


if __name__ == '__main__':
    traceFiles = [ TraceFile( traceFilename ) for traceFilename in traceFilenames ]
    readyFiles = getReadyFiles( traceFiles )
    while readyFiles != []:
        if debug > 0:
            print "Ready files:"
        for f in readyFiles:
            if debug > 0:
                print f.traceFilename
        readReadyFiles( readyFiles )
        readyFiles = getReadyFiles( traceFiles )
        #x = raw_input()
    if debug > 0:
        for traceFile in traceFiles:
            print "%s: %d, %d" % ( traceFile.traceFilename, traceFile.eventNumber, traceFile.registeredEvents )

