from constants import *

######################################################################
## SENTENCE CLASS
class Sentence():
    def __init__(self, name, which, theparasub, thesentsub, \
                 thesent, thetaggedsent, stopwords):
        self._name = name
        self._which = which
        self._parasub = theparasub;
        self._sentsub = thesentsub;
        self._thesent = thesent;
        self._thetaggedsent = thetaggedsent;

        self._alignmentlevel = -1
        self._alignmentpara = ALIGNMENTDUMMYPARA
        self._alignmentsub = ALIGNMENTDUMMYSUB

        self._distance = DISTANCEDUMMY
        self._previousdistance = -1
        self._editdistfracofworst = -1.0

        self._bag = set()
        self._intersection = set()
        self._bagsizefrac = -1.0
        self._othersentencebagsize = 0
        self._othersentencebagsizefrac = -1.0

#        self._stopwords = stopwords
        self.createbagofwords(stopwords)

######################################################################
##
    def __eq__(self, other):
        return self._thesent == other._thesent
######################################################################
##
    def __ge__(self, other):
        return self._thesent >= other._thesent
######################################################################
##
    def __gt__(self, other):
        return self._thesent > other._thesent
######################################################################
##
    def __le__(self, other):
        return self._thesent <= other._thesent
######################################################################
##
    def __lt__(self, other):
        return self._thesent < other._thesent

######################################################################
##
    def __str__(self):
        if 'DRAFT' == self._which:
            s = '%s %s %2d ( %2d - %3d ) ( %2d - %3d ) %4d %4d %6.3f  %4d   %4d %4d %4d %6.3f %6.3f'%\
                 (self._name, self._which, self._alignmentlevel, \
                  self._parasub, self._sentsub, \
                  self._alignmentpara, self._alignmentsub, \
                  self._previousdistance, \
                  self._distance, self._editdistfracofworst, \
                  len(self._thesent), \
                  len(self._bag), self._othersentencebagsize, \
                  len(self._intersection), \
                  self._bagsizefrac, self._othersentencebagsizefrac)

            if self.isaligned():
                s += ' ALI_YES____'
            else:
                s += ' ALI_____NO '

            if self.isdeletion():
                s += ' DEL_YES____'
            else:
                s += ' DEL_____NO '

            if self.isinsertion():
                s += ' INS_YES____'
            else:
                s += ' INS_____NO '

#            if self._misaligned:
#                s += ' MIS_YES'
#            else:
#                s += ' MIS_NO '

#            s += '                SENTENCE %s\n' % (self.stringit(self._thesent))
#            s += '                     BAG %s' % (self.stringit(self._bag))

        elif 'FINAL' == self._which:
            s = '%s %s %2d ( %2d - %3d ) ( %2d - %3d ) %4d %4d %6.3f  %4d   %4d %4d %4d %6.3f %6.3f'%\
                 (self._name, self._which, self._alignmentlevel, \
                  self._alignmentpara, self._alignmentsub, \
                  self._parasub, self._sentsub, \
                  self._previousdistance, \
                  self._distance, self._editdistfracofworst, \
                  len(self._thesent), \
                  self._othersentencebagsize, len(self._bag), \
                  len(self._intersection), \
                  self._othersentencebagsizefrac, self._bagsizefrac)

            if self.isaligned():
                s += ' ALI_YES____'
            else:
                s += ' ALI_____NO '

            if self.isdeletion():
                s += ' DEL_YES____'
            else:
                s += ' DEL_____NO '

            if self.isinsertion():
                s += ' INS_YES____'
            else:
                s += ' INS_____NO '

#            if self._misaligned:
#                s += ' MIS_YES'
#            else:
#                s += ' MIS_NO '

#            s += '                SENTENCE %s\n' % (self.stringit(self._thesent))
#            s += '                     BAG %s' % (self.stringit(self._bag))
        return s

######################################################################
## create a set as a bag of words
## yes, used
    def createbagofwords(self, stopwords):

        for self._word in self._thesent:
            if self._word not in stopwords:
                self._bag.add(self._word)
#        return self._bag

######################################################################
## yes, used
    def formatsub(self, thesub):
        self._s = 'FORMAT'
        if self._sentsub != thesub:
            self._s = 'ERROR IN FORMATSUB %d %d' % (self._sentsub, thesub)
            return self._s
        if self._sentsub < 10:
            self._ssent = '_%d' % (self._sentsub)
        else:
            self._ssent = '%2d' % (self._sentsub)

        if self._parasub < 10:
            self._spara = ' %d' % (self._parasub)
        else:
            self._spara = '%2d' % (self._parasub)
        self._s = self._spara + '-' + self._ssent
        return self._s

######################################################################
## yes, used
    def getalignmentlevel(self):
        return self._alignmentlevel

######################################################################
##
    def getalignmentpara(self):
        return self._alignmentpara

######################################################################
## yes, used
    def getalignmentsub(self):
        return self._alignmentsub


######################################################################
## yes, used
    def getbagofwords(self):
        return self._bag

######################################################################
## yes, used
    def getbagsizefrac(self):
        return self._bagsizefrac

######################################################################
## yes, used
    def getdistance(self):
        return self._distance

######################################################################
## yes, used
    def geteditdistfracofworst(self):
        return self._editdistfracofworst

######################################################################
## yes, used
    def getlenbag(self):
        return len(self._bag)

######################################################################
## yes, used
    def getleninter(self):
        return len(self._intersection)

######################################################################
## yes, used
    def getlength(self):
        return len(self._thesent)

######################################################################
## yes, used
    def getparasub(self):
        return self._parasub

######################################################################
## yes, used
    def getpreviousdistance(self):
        return self._previousdistance

######################################################################
## yes, used
    def getsent(self):
        return self._thesent

######################################################################
## yes, used
    def getsentsub(self):
        return self._sentsub

######################################################################
##
    def gettaggedsent(self):
        return self._thetaggedsent

######################################################################
## yes, used
    def isaligned(self):
#        print('%4d %4d' % (self._sentsub, self._alignmentsub))
        return (ALIGNMENTDUMMYSUB != self._alignmentsub)

######################################################################
## yes, used
    def isdeletion(self):
        return ('DRAFT' == self._which) and (ALIGNMENTDUMMYSUB == self._alignmentsub)

######################################################################
## yes, used
    def isinsertion(self):
        return ('FINAL' == self._which) and (ALIGNMENTDUMMYSUB == self._alignmentsub)

######################################################################
## yes, used
    def setalignment(self, whatlevel, othersentence, distance):
        # set subscript pointers to the aligned sentence
        self._alignmentlevel = whatlevel
        self._alignmentsub = othersentence.getsentsub()
        self._alignmentpara = othersentence.getparasub()

        # set the distance to the aligned sentence
        self._distance = distance

        # compute edit dist fraction of worst possible
        self._sumoflengths = self.getlength() + othersentence.getlength()
        if self._sumoflengths > 0:
            self._editdistfracofworst = float(distance) / float(self._sumoflengths)
        else:
            self._editdistfracofworst = 0.0

        # compute bag of words overlap to the aligned sentence
        self._intersection = self._bag.intersection(othersentence.getbagofwords())
        self._othersentencebagsize = len(othersentence.getbagofwords())
        self._leninter = len(self._intersection)
        if len(self._bag) > 0:
            self._bagsizefrac = float(self._leninter)/float(len(self._bag))
        else:
            self._bagsizefrac = 1.0

        if self._othersentencebagsize > 0:
            self._othersentencebagsizefrac = float(self._leninter)/ \
                                               float(self._othersentencebagsize)
        else:
            self._othersentencebagsizefrac = 1.0

######################################################################
## yes, used
    def setbagsizefrac(self, whatfrac):
        self._bagsizefrac = whatfrac

######################################################################
## yes, used
    def setpreviousdistance(self, what):
        self._previousdistance = what

######################################################################
##
    def stringit(self, what):
        s = ''
        for item in what:
            s += ' ' + item

        return s

######################################################################
##
    def stringthesent(self):
        if 'DRAFT' == self._which:
            s = '%s %s %2d ( %2d - %3d ) ( %2d - %3d ) '% \
                 (self._name, self._which, self._alignmentlevel, \
                  self._parasub, self._sentsub, \
                  self._alignmentpara, self._alignmentsub)

        elif 'FINAL' == self._which:
            s = '%s %s %2d ( %2d - %3d ) ( %2d - %3d ) '% \
                 (self._name, self._which, self._alignmentlevel, \
                  self._alignmentpara, self._alignmentsub, \
                  self._parasub, self._sentsub)

        s += self.stringit(self._thesent)
        return s

## END OF SENTENCE CLASS
######################################################################

