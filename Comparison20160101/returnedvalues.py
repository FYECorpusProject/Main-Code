from constants import *
from collections import defaultdict
#from alignedsentence import AlignedSentence

######################################################################
## RETURNED VALUES FROM ALIGNMENT CLASS
######################################################################
class ReturnedValues():
    def __init__(self):
        self._alignmentdict = defaultdict(int)
        self._deletionsbypara = defaultdict(int)
        self._insertionsbydist = defaultdict(int)
        self._insertionsbypara = defaultdict(int)
        self._listofalignedsentences = []
        self._listofalignedsentencesbydist = []
        self._misalignments = 0

######################################################################
##
    def __str__(self):
        print('str function not yet implemented')
        return ''

######################################################################
##
    def getalignmentdict(self):
        return self._alignmentdict

######################################################################
##
    def incrementalignmentdict(self, keystring):
#        print('increment align %s\n' % keystring)
        self._alignmentdict[keystring] += 1

######################################################################
##
    def incrementalignmentdictnew(self, name, which, sent):
 #       print('increment align %s %s %s\n' % (name, which, sent))
        localkey = '%14s %4d' % ('DUMMY', 9999)
        if 'FINAL' == which:
            localkey = '%14s %4d' % (name, INSERTSUB)
        elif 'DRAFT' == which:
            if not sent.isaligned():
                localkey = '%14s %4d' % (name, DELETESUB)
            else:
                wcf = sent.geteditdistfracofworst()
                localkey = '%14s %4d' % (name, int((wcf+0.005)*100))

        self._alignmentdict[localkey] += 1

######################################################################
##
    def incrementstats(self, name, which, sent):
#        print('increment align %s %s %s' % (name, which, sent))

        dictkey = '%14s %4d' % ('DICTDUMMY', 9999)
        parakey = '%14s %4d' % ('PARADUMMY', 9999)

        if 'FINAL' == which:
            if not sent.isaligned():
                dictkey = '%14s %4d' % (name, INSERTSUB)
                parakey = '%14s %4d' % (name, sent.getparasub())
                self._insertionsbypara[parakey] += 1
        elif 'DRAFT' == which:
            if not sent.isaligned():
                dictkey = '%14s %4d' % (name, DELETESUB)
                parakey = '%14s %4d' % (name, sent.getparasub())
                self._deletionsbypara[parakey] += 1
            else:
                wcf = sent.geteditdistfracofworst()
                dictkey = '%14s %4d' % (name, int((wcf+0.005)*100))

#        print('increment align %s %s "%s" %s\n' % (name, which, dictkey, sent))
        self._alignmentdict[dictkey] += 1

######################################################################
##
    def getdeletionsbypara(self):
        return self._deletionsbypara

######################################################################
##
    def incrementdeletionsbypara(self, keystring):
#        print('increment dele %s\n' % keystring)
        self._deletionsbypara[keystring] += 1

######################################################################
##
    def getinsertionsbydist(self):
        return self._insertionsbydist

######################################################################
##
    def incrementinsertionsbydist(self, keystring):
#        print('increment dist %s\n' % keystring)
        self._insertionsbydist[keystring] += 1

######################################################################
##
    def getinsertionsbypara(self):
        return self._insertionsbypara

######################################################################
##
    def incrementinsertionsbypara(self, keystring):
#        print('increment para %s\n' % keystring)
        self._insertionsbypara[keystring] += 1

######################################################################
##
    def getlistofalignedsentences(self):
        return self._listofalignedsentences

######################################################################
##
    def getlistofalignedsentencesbydist(self):
        return self._listofalignedsentences

######################################################################
##
    def addtolistofalignedsentences(self, thislistitem):
        newalignedsentence = AlignedSentence(thislistitem)
        self._listofalignedsentences.append(newalignedsentence)

######################################################################
##
    def getmisalignments(self):
        return self._misalignments

######################################################################
##
    def incrementmisalignments(self):
        self._misalignments += 1

######################################################################
## END OF RETURNED VALUES FROM ALIGNMENT CLASS
######################################################################
