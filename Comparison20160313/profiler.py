######################################################################
## LINGUISTIC PROFILER CLASS
import nltk
import sys
from nltk.tag import pos_tag

from collections import defaultdict
from dabfunctions import printoutput
from sentence import Sentence

class LinguisticProfiler():

    def __init__(self, stopwords):
        self._globalmostfreq = defaultdict(int)
        self._globalmostfreqpos = defaultdict(int)
        self._globalmostfreqposbywords = defaultdict(int)
        self._globalmostfreqposandwords = defaultdict(list)
        self._globalmostfreqreporting = defaultdict(int)
        self._TAG = 'PROFILER'
        self._stopwords = set(stopwords)
        thefile = open('reporting_verbs.txt')
        self._reporting = set(thefile.read().split())
#        print(self._reporting)

######################################################################
##
    def __str__(self):
        label = 'ZORKPROFILE'
        s = '%s LINGUISTIC PROFILE' % (label)
        flippeddict = []
        for key, value in self._globalmostfreq.items():
            flippeddict.append([value, key])

        for item in sorted(flippeddict):
            s += '%s %6d %s\n' % (label, item[0], item[1])

        return s

######################################################################
## do the profile for a list of instances of 'sentence'
    def doprofile(self, name, which, sents, outfile):
        wordcount = 0
        wordset = set()
        mostfreq = defaultdict(int)
        mostfreqpos = defaultdict(int)
        mostfreqposbywords = defaultdict(int)
        mostfreqposandwords = defaultdict(list)
        mostfreqreporting = defaultdict(int)
#       remember the sentence count is bogus high by two for dummy sents
        for sub, s in enumerate(sents):

            # skip the bogus sentences
            # this is the easy part, just printing sentence lengths
            if (sub == 0) or (sub == len(sents)-1):
                outstring = '%s %s ZORKSENTENCELENGTH%s %4d %4d DUMMY' % \
                            (name, self._TAG, which, sub, s.getlength())
                printoutput(outstring, outfile)
                continue
            else:
                outstring = '%s %s ZORKSENTENCELENGTH%s %4d %4d' % \
                            (name, self._TAG, which, sub, s.getlength())
                printoutput(outstring, outfile)

            # we do sets of words to be able to do the lex diversity
            wordcount += s.getlength()
            wordset = wordset.union(set(s.getsent()))

            # collect frequencies of words and pos
            taggedsentence = pos_tag(s.getsent())
            for item in taggedsentence:
                word = item[0]
                partofspeech = item[1]

                if ',' == word:
#                    outstring = '%s %s COMMA %s' % (name, self._TAG, item)
#                    printoutput(outstring, outfile)
                    continue
                if '.' == word: continue
                if '``' == word: continue
                if "''" == word: continue
                if "'" == word: continue
                if "?" == word: continue

                if 'NNP' == partofspeech:
                    wordkey = word
                else:
                    wordkey = word.lower()

                ssssuuuu = '%s_%s' % (wordkey, partofspeech)
                mostfreqposbywords[ssssuuuu] += 1
                self._globalmostfreqposbywords[ssssuuuu] += 1

                mostfreqpos[partofspeech] += 1
                self._globalmostfreqpos[partofspeech] += 1

                mostfreq[wordkey] += 1
                self._globalmostfreq[wordkey] += 1
                mostfreqposandwords[partofspeech].append(wordkey)
                self._globalmostfreqposandwords[partofspeech].append(wordkey)

                if wordkey in self._reporting:
                    mostfreqreporting[wordkey] += 1
                    self._globalmostfreqreporting[wordkey] += 1

        # print the lex diversity for this doc
        outstring = '%s %s ZORKDIVERSITY%s %5d %4d %4d %8.3f' % \
                      (name, self._TAG, which, len(sents)-2, \
                      wordcount, len(wordset), \
                      float(len(wordset)) / float(wordcount))
        printoutput(outstring, outfile)

        howmany = 10
        # print the most freq nonstopwords for this doc
        self.printflippeddict(name, 'ZORKMOSTFREQ', which, mostfreq, howmany, outfile)

        # print the most freq parts of speech for this doc
        self.printflippeddict(name, 'ZORKMOSTFREQPOS', which, mostfreqpos, howmany, outfile)

        # print the most freq parts of speech with words for this doc
        self.printflippeddict(name, 'ZORKMOSTFREQPOSBYWORDS', which, mostfreqposbywords, howmany, outfile)

        # print the most freq reporting verbs
        self.printflippeddict(name, 'ZORKMOSTFREQREPORTING', which, mostfreqreporting, howmany, outfile)

        # print the most freq parts of speech for this doc
        # long form with the actual words
        for key, value in sorted(mostfreqposandwords.items()):
            localdict = defaultdict(int)
            for token in value:
                localdict[token.lower()] += 1
            locallist = []
            for localkey, localvalue in localdict.items():
                locallist.append([localvalue, localkey])
#            outstring = '%s %s ZORKMOSTFREQPOSWORDS%s %-6s %s' % (name, self._TAG, which, key, value)
            outstring = '%s %s ZORKMOSTFREQPOSWORDS%s %-6s' % \
                           (name, self._TAG, which, key)
            for item in reversed(sorted(locallist)):
                outstring += ' %s:%d' % (item[1], item[0])
            printoutput(outstring, outfile)

######################################################################
## start with a dict of freqs and return the breakpoint such that
## freq > breakpoint returns the howmany-th largest values
## 
## create a set of the actual values 
## turn the set into a list
## sort the list
## slice the howmany-th values
## and take the last one
    def getbreakpointforlargest(self, thedict, howmany):
        valueset = set()
        for key, value in thedict.items():
            if key not in self._stopwords:
                valueset.add(value)
#        print('SET     %s' % (valueset))
        valuelist = sorted(list(valueset))
#        print('LIST    %s' % (valuelist))
        valuelist.reverse()
#        print('REVERSE %s' % (valuelist))
        valuelistslice = valuelist[:howmany]
#        print('SLICE   %s' % (valuelistslice))
        valuelistslice.reverse()
        if len(valuelistslice) > 0:
            breakpoint = valuelistslice[0]
        else:
            breakpoint = -1
#        print('BREAK   %d' % (breakpoint))
        return breakpoint

#######################################################################
###
#    def getglobalmostfreq(self):
#        return self._globalmostfreq

######################################################################
##
    def printglobalresults(self, name, which, outfile):
        howmany = 10
        # print the most freq nonstopwords for this doc
        self.printflippeddict(name, 'ZORKGLOBALMOSTFREQ', which, self._globalmostfreq, howmany, outfile)

        # print the most freq parts of speech for this doc
        self.printflippeddict(name, 'ZORKGLOBALMOSTFREQPOS', which, self._globalmostfreqpos, howmany, outfile)

        # print the most freq parts of speech with words for this doc
        self.printflippeddict(name, 'ZORKGLOBALMOSTFREQPOSBYWORDS', which, self._globalmostfreqposbywords, howmany, outfile)
        # print the most freq reporting verbs
        self.printflippeddict(name, 'ZORKGLOBALMOSTFREQREPORTING', which, self._globalmostfreqreporting, howmany, outfile)

        # print the most freq parts of speech for this doc
        # long form with the actual words
        for key, value in sorted(self._globalmostfreqposandwords.items()):
            localdict = defaultdict(int)
            for token in value:
                localdict[token.lower()] += 1
            locallist = []
            for localkey, localvalue in localdict.items():
                locallist.append([localvalue, localkey])
                outstring = '%s %s ZORKGLOBALMOSTFREQPOSWORDS%s %-6s' % \
                           (name, self._TAG, which, key)
            for item in reversed(sorted(locallist)):
                outstring += ' %s:%d' % (item[1], item[0])
            printoutput(outstring, outfile)

######################################################################
##
    def printflippeddict(self, name, label, which, thedict, howmany, outfile):
        flippeddict = []
        for key, value in thedict.items():
            flippeddict.append([value, key])

        breakpoint = self.getbreakpointforlargest(thedict, howmany)

        for item in sorted(flippeddict):
            if item[1] not in self._stopwords:
                if item[0] >= breakpoint:
                    outstring = '%s %s %s%s %5d %s' % (name, self._TAG, label, which, item[0], item[1])
                    printoutput(outstring, outfile)


## END OF LINGUISTIC PROFILER CLASS
######################################################################

