import sys
ALIGNMENTDUMMYPARA = -9
ALIGNMENTDUMMYSUB = -99
DISTANCEDUMMY = -999

######################################################################
## HISTOSENTENCE CLASS
class HistoSentence():
    def __init__(self, line):
        lineSplit = line.split()

        self._name = lineSplit[1]
        self._which = lineSplit[2]
        self._alignmentLevel = int(lineSplit[3])
        self._leftParaSub = int(lineSplit[5])
        self._leftSentSub = int(lineSplit[7])
        self._rightParaSub = int(lineSplit[10])
        self._rightSentSub = int(lineSplit[12])
        self._previousDistance = int(lineSplit[14])
        self._distance = int(lineSplit[15])
        self._editDistFracOfWorst = float(lineSplit[16])

        self._sentenceLength = int(lineSplit[17])

        self._leftSentBagSize = int(lineSplit[18])
        self._rightSentBagSize = int(lineSplit[19])
        self._intersectionBagSize = int(lineSplit[20])
        self._leftBagSizeFrac = float(lineSplit[21])
        self._rightBagSizeFrac = float(lineSplit[22])
        self._alignedTag = lineSplit[23]
        self._deletedTag = lineSplit[24]
        self._insertedTag = lineSplit[25]

######################################################################
##
    def __str__(self):
        s = 'HH %s %s %2d ( %2d - %3d ) ( %2d - %3d ) %4d %4d %6.3f  %4d   %4d %4d %4d %6.3f %6.3f %-11s %-11s %-11s'%\
             (self._name, self._which, self._alignmentLevel, \
              self._leftParaSub, self._leftSentSub, \
              self._rightParaSub, self._rightSentSub, \
              self._previousDistance, \
              self._distance, self._editDistFracOfWorst, \
              self._sentenceLength, \
              self._leftSentBagSize, self._rightSentBagSize, \
              self._intersectionBagSize, \
              self._leftBagSizeFrac, self._rightBagSizeFrac, \
              self._alignedTag, self._deletedTag, self._insertedTag)

        return s

######################################################################
##
    def checkAlignedSentences(self, thatSent):
#        print(thatSent)
#        print(thatSent.getLeftParaSub())
        checksout = True
        if self._leftParaSub != thatSent.getLeftParaSub():
            checksout = False
        if self._leftSentSub != thatSent.getLeftSentSub():
            checksout = False
        if self._rightParaSub != thatSent.getRightParaSub():
            checksout = False
        if self._rightSentSub != thatSent.getRightSentSub():
            checksout = False

        if not checksout:
            print('ERROR AlignedSentences %s' % (self))
            sys.exit()


######################################################################
##
    def checkInternalCorrectness(self):

        # if it says it's a deletion, then right should be dummy
        if 'DEL_YES____' == self._deletedTag:
            if ALIGNMENTDUMMYPARA != self._rightParaSub:
                print('ERROR Deletion A1 %s' % (self))
                sys.exit()
            if ALIGNMENTDUMMYSUB != self._rightSentSub:
                print('ERROR Deletion A2 %s' % (self))
                sys.exit()
            if 'DRAFT' != self._which:
                print('ERROR Deletion A3 %s' % (self))
                sys.exit()
            if 'ALI_YES____' == self._alignedTag:
                print('ERROR Deletion A4 %s' % (self))
                sys.exit()
                
        elif 'DEL_____NO' == self._deletedTag:
            if ALIGNMENTDUMMYPARA == self._rightParaSub:
                print('ERROR Deletion B1 %s' % (self))
                sys.exit()
            if ALIGNMENTDUMMYSUB == self._rightSentSub:
                print('ERROR Deletion B2 %s' % (self))
                sys.exit()
        else:
                print('ERROR C %s' % (self))
                sys.exit()

        # if it says it's an insertion, then left should be dummy
        if 'INS_YES____' == self._insertedTag:
            if ALIGNMENTDUMMYPARA != self._leftParaSub:
                print('ERROR Insertion D1 %s' % (self))
                sys.exit()
            if ALIGNMENTDUMMYSUB != self._leftSentSub:
                print('ERROR Insertion D2 %s' % (self))
                sys.exit()
            if 'FINAL' != self._which:
                print('ERROR Insertion D3 %s' % (self))
                sys.exit()
            if 'ALI_YES____' == self._alignedTag:
                print('ERROR Insertion D4 %s' % (self))
                sys.exit()
                
        elif 'INS_____NO' == self._insertedTag:
            if ALIGNMENTDUMMYPARA == self._leftParaSub:
                print('ERROR Insertion E1 %s' % (self))
                sys.exit()
            if ALIGNMENTDUMMYSUB == self._leftSentSub:
                print('ERROR Insertion E2 %s' % (self))
                sys.exit()
        else:
                print('ERROR F %s' % (self))
                sys.exit()

        # if it says it's aligned, then it should be aligned
        if 'ALI_YES____' == self._alignedTag:
            if ALIGNMENTDUMMYPARA == self._leftParaSub:
                print('ERROR Alignment G1 %s' % (self))
                sys.exit()
            if ALIGNMENTDUMMYSUB == self._leftSentSub:
                print('ERROR Alignment G2 %s' % (self))
                sys.exit()
            if ALIGNMENTDUMMYPARA == self._rightParaSub:
                print('ERROR Alignment G3 %s' % (self))
                sys.exit()
            if ALIGNMENTDUMMYSUB == self._rightSentSub:
                print('ERROR Alignment G4 %s' % (self))
                sys.exit()

######################################################################
##
    def formatSub(self, theSub):
        self._s = 'FORMAT'
        if self._sentSub != theSub:
            self._s = 'ERROR IN FORMATSUB %d %d' % (self._sentSub, theSub)
            return self._s
        if self._sentSub < 10:
            self._sSent = '_%d' % (self._sentSub)
        else:
            self._sSent = '%2d' % (self._sentSub)

        if self._paraSub < 10:
            self._sPara = ' %d' % (self._paraSub)
        else:
            self._sPara = '%2d' % (self._paraSub)
        self._s = self._sPara + '-' + self._sSent
        return self._s

######################################################################
##
    def getAlignmentLevel(self):
        return self._alignmentLevel

######################################################################
##
    def getBagOfWords(self):
        return self._bag

######################################################################
##
    def getBagSizeFrac(self):
        return self._bagSizeFrac

######################################################################
##
    def getDistance(self):
        return self._distance

######################################################################
##
    def getEditDistFracOfWorst(self):
        return self._editDistFracOfWorst

######################################################################
##
    def getLeftParaSub(self):
        return self._leftParaSub

######################################################################
##
    def getLeftSentSub(self):
        return self._leftSentSub

######################################################################
##
    def getLenBag(self):
        return len(self._bag)

######################################################################
##
    def getName(self):
        return self._name

######################################################################
##
    def getRightParaSub(self):
        return self._rightParaSub

######################################################################
##
    def getRightSentSub(self):
        return self._rightSentSub

######################################################################
##
    def getLenInter(self):
        return len(self._intersection)

######################################################################
##
    def getPreviousDistance(self):
        return self._previousDistance

######################################################################
##
    def getSentenceLength(self):
        return self._sentenceLength

######################################################################
##
    def getType(self):
        return int(self._name[-1])

######################################################################
##
    def getWhich(self):
        return self._which

######################################################################
##
    def isAligned(self):
        if 'DRAFT' == self._which:
            return (ALIGNMENTDUMMYSUB != self._rightSentSub)
        else:
            return (ALIGNMENTDUMMYSUB != self._leftSentSub)

######################################################################
##
    def isDeletion(self):
        return ('DRAFT' == self._which) and (ALIGNMENTDUMMYSUB == self._alignmentSub)

######################################################################
##
    def isInsertion(self):
        return ('FINAL' == self._which) and (ALIGNMENTDUMMYSUB == self._alignmentSub)

######################################################################
##
    def stringIt(self, what):
        s = ''
        for item in what:
            s += ' ' + item

        return s

## END OF SENTENCE CLASS
######################################################################

