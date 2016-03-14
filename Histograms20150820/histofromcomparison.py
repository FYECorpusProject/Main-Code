#!/usr/bin/env python ## use python 2.7

import sys
from collections import defaultdict
from os import listdir
from histogramcode import Histogram
from histosentence import HistoSentence
##
import numpy as np
import matplotlib.pyplot as plt

ALIGNMENTDUMMYPARA = -9
ALIGNMENTDUMMYSUB = -99
DISTANCEDUMMY = -999

######################################################################
## FUNCTIONS

######################################################################
## check arguments
def checkArgs(number, message):
    if len(sys.argv) != number:
        print(message)
        sys.exit(1)

######################################################################
## filter the data by type and category
## 'ALIGN', 'DELETIONS', 'INSERTIONS', and types 1, 2, 3, or 4
def filterTheData(theData, whichEvent, whichType, alignChoice=0):
    histoDict = defaultdict(int)
    for line in theData:
#        print('FILTERA %s' % (line))
        if whichEvent not in line[0]: continue
#        print('FILTERB %s' % (line))
        if (whichType == 0) or (whichType == int(line[2])):
#            print('FILTERC %s' % (line))

            if ('EDITDISTS' in whichEvent) or \
               ('INSERTBYDIST' in whichEvent) or \
               ('INSERTIONS' in whichEvent) or \
               ('DELETIONS' in whichEvent):
#                print('FILTERD %s' % (line))
                histoDict[int(line[3])] += int(line[4])

            if ('SENTENCELENGTHDRAFT' in whichEvent) or \
               ('SENTENCELENGTHFINAL' in whichEvent):
#                print('FILTERE %s' % (line))
                histoDict[int(line[3])] += 1

            if ('ALIGNMENT_COUNT' in whichEvent):
                if 0 == alignChoice:
#                    print('FILTERE %s' % (line))
#                   subtract 1 from value because we want the number of
#                   useful phases and not the phase when nothing happened
                    histoDict[int(line[3])-1] += 1

                if 1 == alignChoice:
#                    print('FILTERF %s' % (line))
#                   subtract 1 from value because we want the number of
#                   useful phases and not the phase when nothing happened
                    sentCount = int(line[4]) + int(line[5]) # draft 
                    if 0 != sentCount:
                        fractionAligned = 100.0 * float(line[4]) / float(sentCount)
                    else:
                        fractionAligned = 0.0
#                    print('FILTERF %d %d %d %f' % (int(line[4]), int(line[5]), int(line[6]), fractionAligned))
                    histoDict[int(fractionAligned)] += 1

                if 2 == alignChoice:
#                    print('FILTERG %s' % (line))
#                   subtract 1 from value because we want the number of
#                   useful phases and not the phase when nothing happened
                    sentCount = int(line[4]) + int(line[6]) # final 
                    if 0 != sentCount:
                        fractionAligned = 100.0 * float(line[4]) / float(sentCount)
                    else:
                        fractionAligned = 0.0
#                    print('FILTERG %d %d %d %f' % (int(line[4]), int(line[5]), int(line[6]), fractionAligned))
                    histoDict[int(fractionAligned)] += 1

    return histoDict

######################################################################
## filter the data by type and category
## 'ALIGN', 'DELETIONS', 'INSERTIONS', and types 1, 2, 3, 4, ...
def filterTheData2(theData, whichEvent, whichType, whichVersion):
    histoDict = defaultdict(int)
    for line in theData:
#        print('FILTERA %s' % (line))
        if whichEvent not in line[0]: continue
#        print('FILTERB %s' % (line))
        if (whichType == 0) or (whichType == int(line[2])):
#            print('FILTERC %s' % (line))

            if ('SENTENCECOUNTS' in whichEvent) or \
               ('PARACOUNTS' in whichEvent):
#                print('FILTERE %s' % (line))
                if whichVersion == 'draft':
                    histoDict[int(line[3])] += 1
                elif whichVersion == 'final':
                    histoDict[int(line[4])] += 1
                else:
                    print('ERROR IN VERSION CHOICE filterTheData2 %s' % (whichVersion))
                    sys.exit()

    return histoDict

######################################################################
## alignment counts and fractions by level histogram code
def histoAlignmentFractionsByLevel(theData, theType, which, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        name = sent.getName()
        level = int(sent.getAlignmentLevel())
        if -1 == level: level = 999
        localDict[level] += 1

#    for level, freqs in sorted(localDict.items()):
#        print('%5d %5d' % (level, freqs))

    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo += 'Column 1: fraction aligned in '+ which + '\n'
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'ALIGNMENTS FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict, 1, 1, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO PAPERS FOR %s\n' % (label))
        outFile.write('NO PAPERS FOR %s\n' % (label))

######################################################################
## alignment levels histogram code
def histoAlignmentLevels(theData, theType, which, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        name = sent.getName()
        level = int(sent.getAlignmentLevel())

        if level > localDict[name]:
            localDict[name] = level

    localDict2 = defaultdict(int)
    for name, maxValue in sorted(localDict.items()):
#        print('%6s %5d' % (name, maxValue))
        localDict2[maxValue] += 1

#    for levels, freqs in sorted(localDict2.items()):
#        print('%5d %5d' % (levels, freqs))

    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo += 'Column 1: last alignment with changes\n'
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'LAST ALIGNMENT FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict2) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict2, 1, 1, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO ALIGNMENTS FOR %s\n' % (label))
        outFile.write('NO ALIGNMENTS FOR %s\n' % (label))

######################################################################
## deletions by paragraph histogram code
def histoDeletionsByPara(theData, theType, which, lastParaNumDict, theFilter, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        if sent.isAligned(): continue
        paraNum = sent.getLeftParaSub()
        docName = key.split()[0]
        lastParaKey = docName + ' ' + which
        lastParaNum = lastParaNumDict[lastParaKey]

        if ('FIRST' == theFilter) and (0 != paraNum): continue
        if ('LAST' == theFilter) and (lastParaNum != paraNum):
            continue
        if ('MIDDLE' == theFilter):
            if (0 == paraNum) or (lastParaNum == paraNum):
                continue

        localDict[paraNum] += 1

#    for dist, freq in sorted(localDict.items()):
#        print('%5d %5d' % (dist, freq))

    headerInfo = '\nInput from file: %s for %s\n' % (inFileName, theFilter)
    headerInfo += 'Column 1: paragraph numbers\n'
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'DELETIONS BY PARAGRAPH FROM DRAFT FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict, 1, 1, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO DELETIONS FOR %s\n' % (label))
        outFile.write('NO DELETIONS FOR %s\n' % (label))

######################################################################
## edit distance histogram code
def histoEditDistance(theData, theType, which, lastParaNumDict, theFilter, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        if 'DRAFT' == which:
            paraNum = sent.getLeftParaSub()
        else:
            paraNum = sent.getRightParaSub()
        docName = key.split()[0]
        lastParaKey = docName + ' ' + which
        lastParaNum = lastParaNumDict[lastParaKey]

        if ('FIRST' == theFilter) and (0 != paraNum): continue
        if ('LAST' == theFilter) and (lastParaNum != paraNum):
            continue
        if ('MIDDLE' == theFilter):
            if (0 == paraNum) or (lastParaNum == paraNum):
                continue

        distRounded = int(round(sent.getEditDistFracOfWorst() * 100.0))
        if distRounded < 0: distRounded = 999
        localDict[distRounded] += 1

#    for dist, freq in sorted(localDict.items()):
#        print('%5d %5d' % (dist, freq))

    headerInfo = '\nInput from file: %s for %s\n' % (inFileName, theFilter)
    headerInfo += 'Column 1: % change in aligned sentences from draft to final\n'
    headerInfo += "          'UNALIGN' means deletions from draft, insertions into final\n"
    headerInfo += 'Column 2: % of sentences with that change\n'
    headerInfo += 'Column 3: raw numbers of sentences with that change\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'EDIT DISTANCE COMPARISONS FOR ' + which + ' OF TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict, 4, 4, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO EDIT DIST FRACS FOR %s\n' % (label))
        outFile.write('NO EDIT DIST FRACS FOR %s\n' % (label))




    if 0 != theType: return

    localTypeListDict = defaultdict(list)
    for key in range(0, 5): 
        localTypeListDict[key] = [0] 

    for key, sent in sorted(theData.items()):
        if which != sent.getWhich(): continue
        thisType = sent.getType()

        distRounded = int(round(sent.getEditDistFracOfWorst() * 100.0))
        if distRounded < 0: distRounded = -5

        # do the actual type
        thisList = localTypeListDict[thisType]
        thisList.append(distRounded)
        localTypeListDict[thisType] = thisList

        # do the "all" type, which is type 0
        thisList = localTypeListDict[0]
        thisList.append(distRounded)
        localTypeListDict[0] = thisList


    multiset = []
    for key, value in sorted(localTypeListDict.items()):
        multiset.append(value)
#        print('TYPE %d' % (key))
#        print('type %d %s' % (key, value))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    numBins = 50
    numBins = 25

    ax.hist(multiset, numBins, color=['green','red','blue','lime','orange'], \
            label = ['0', '1', '2', '3', '4'], alpha=0.8)
    ax.legend(prop={'size': 10})
    ax.set_title('Edit Distance Histograms ' + which)
#    plt.show()
    plt.savefig('EditDistHistograms' + which)


######################################################################
## insertions by edit dist frac of previous
def histoInsertionsByEditDistFrac(theData, theType, which, outFile):
    paperSet = set()
    paperCount = 0
    beginningInsertionCount = 0
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue

        keySplit = key.split()
        paperSet.add(keySplit[0])
        
        if sent.isAligned(): continue
        prevDist = sent.getPreviousDistance()
        if prevDist < 0:
            prevDist = 899
            if 'FINAL' == which:
                if 0 == sent.getRightParaSub() and 0 == sent.getRightSentSub(): 
                    beginningInsertionCount += 1
#                    print('INITIAL INSERTION %s %s' % (key, sent))

        localDict[prevDist] += 1

#    for dist, freq in sorted(localDict.items()):
#        print('%5d %5d' % (dist, freq))

    paperCount = len(paperSet)
#    print('PAPER COUNT %3s' % (paperCount))


    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo += 'There were initial insertions in %3d of %3d papers\n' % \
                 (beginningInsertionCount, paperCount)
    headerInfo += 'Column 1: edit dist fracs before insertion\n'
#    headerInfo += "          the '899' means insertion at beginning of paper\n"
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'INSERTIONS BY EDIT DIST FRAC OF PREVIOUS SENTENCE FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict, 4, 4, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO INSERTIONS FOR %s\n' % (label))
        outFile.write('NO INSERTIONS FOR %s\n' % (label))

######################################################################
## insertions by paragraph histogram code
def histoInsertionsByPara(theData, theType, which, lastParaNumDict, theFilter, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        if sent.isAligned(): continue
        paraNum = sent.getRightParaSub()

        docName = key.split()[0]
        lastParaKey = docName + ' ' + which
        lastParaNum = lastParaNumDict[lastParaKey]
        if ('FIRST' == theFilter) and (0 != paraNum): continue
        if ('LAST' == theFilter) and (lastParaNum != paraNum):
            continue
        if ('MIDDLE' == theFilter):
            if (0 == paraNum) or (lastParaNum == paraNum):
                continue

        localDict[paraNum] += 1

#zork

#    for dist, freq in sorted(localDict.items()):
#        print('%5d %5d' % (dist, freq))
    headerInfo = '\nInput from file: %s for %s\n' % (inFileName, theFilter)
    headerInfo += 'Column 1: paragraph numbers\n'
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'INSERTIONS BY PARAGRAPH INTO FINAL FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict, 1, 1, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO INSERTIONS FOR %s\n' % (label))
        outFile.write('NO INSERTIONS FOR %s\n' % (label))

######################################################################
## paragraph count histogram code
def histoParagraphCounts(theData, theType, which, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        name = sent.getName()
        if 'DRAFT' == which:
            paraNum = int(sent.getLeftParaSub())
        else:
            paraNum = int(sent.getRightParaSub())

        if paraNum > localDict[name]:
            localDict[name] = paraNum

    localDict2 = defaultdict(int)
    for name, maxValue in sorted(localDict.items()):
#        print('%6s %5d' % (name, maxValue))
        localDict2[maxValue] += 1

#    for numParas, freq in sorted(localDict2.items()):
#        print('%5d %5d' % (numParas, freq))

    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo += 'Column 1: # of paragraphs ' + which + '\n'
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'PARAGRAPH COUNTS FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict2) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict2, 1, 1, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO PARAGRAPHS FOR %s\n' % (label))
        outFile.write('NO PARAGRAPHS FOR %s\n' % (label))

######################################################################
## sentence count histogram code
def histoSentenceCounts(theData, theType, which, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        name = sent.getName()
        if 'DRAFT' == which:
            sentNum = int(sent.getLeftSentSub())
        else:
            sentNum = int(sent.getRightSentSub())

        if sentNum > localDict[name]:
            localDict[name] = sentNum

    localDict2 = defaultdict(int)
    for name, maxValue in sorted(localDict.items()):
#        print('%6s %5d' % (name, maxValue))
        localDict2[maxValue] += 1

#    for numSents, freq in sorted(localDict2.items()):
#        print('%5d %5d' % (numSents, freq))

    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo += 'Column 1: # of paragraphs ' + which + '\n'
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'SENTENCE COUNTS FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict2) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict2, 2, 2, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO SENTENCES FOR %s\n' % (label))
        outFile.write('NO SENTENCES FOR %s\n' % (label))

#######################################################################
### sentence length count histogram code
#def histoSentenceLengthCounts(theData, theType, which):
#    localDict = defaultdict(int)
#    for key, sent in sorted(theData.items()):
#        if (0 != theType) and (theType != sent.getType()): continue
#        if which != sent.getWhich(): continue
#        name = sent.getName()
#        if 'DRAFT' == which:
#            sentLen = int(sent.getLength())
#        else:
#            sentLen = int(sent.getLength())
#
#        if sentLen > localDict[name]:
#            localDict[name] = sentLen
#
#    localDict2 = defaultdict(int)
#    for name, maxValue in sorted(localDict.items()):
#        print('%6s %5d' % (name, maxValue))
#        localDict2[maxValue] += 1
#
#    for numSents, freq in sorted(localDict2.items()):
#        print('%5d %5d' % (numSents, freq))
#
#    headerInfo = '\nInput from file: %s\n' % (inFileName)
#    headerInfo += 'Column 1: lengths of sentences (draft)\n'
#    headerInfo += 'Column 2: percent of total\n'
#    headerInfo += 'Column 3: raw numbers of total\n'
#    headerInfo += 'Column 4: the histogram\n'
#    label = 'SENTENCE LENGTHS FOR TYPE %d ' % (theType)
#    label += headerInfo
#
#    if len(localDict2) > 0:
#        histo, shortVersion = Histogram.histoTheData(label, localDict2, 1, 1, fout)
#        print('%s\n' % (histo))
#        fout.write('%s\n' % (histo))
##        shortStuff.append([type, shortVersion])
#    else:
#        print('NO SENTENCE LENGTHS FOR %s\n' % (label))
#        fout.write('NO SENTENCE LENGTHS FOR %s\n' % (label))

######################################################################
## word count histogram code
def histoWordCounts(theData, theType, which, outFile):
    localDict = defaultdict(int)
    for key, sent in sorted(theData.items()):
        if (0 != theType) and (theType != sent.getType()): continue
        if which != sent.getWhich(): continue
        name = sent.getName()
        sentenceLength = sent.getSentenceLength()
        localDict[name] += sentenceLength
#        print('SENT %14s %3d %3d' % (name, sentenceLength, localDict[name]))

    localDict2 = defaultdict(int)
    for name, wordCount in sorted(localDict.items()):
#        print('%6s %5d' % (name, wordCount))
        localDict2[wordCount] += 1

#    for numSents, freq in sorted(localDict2.items()):
#        print('%5d %5d' % (numSents, freq))

    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo += 'Column 1: # of words ' + which + '\n'
    headerInfo += 'Column 2: percent of total\n'
    headerInfo += 'Column 3: raw numbers of total\n'
    headerInfo += 'Column 4: the histogram\n'
    label = 'WORD COUNTS FOR TYPE %d ' % (theType)
    print('%s %s' % (label, which))
    label += headerInfo

    if len(localDict2) > 0:
        histo, shortVersion = Histogram.histoTheData(label, localDict2, 50, 50, outFile)
#        print('%s\n' % (histo))
        outFile.write('%s\n' % (histo))
#        shortStuff.append([type, shortVersion])
    else:
#        print('NO SENTENCES FOR %s\n' % (label))
        outFile.write('NO SENTENCES FOR %s\n' % (label))

######################################################################
## parse the data in a line
def parseTheLine(theLineSplit):
    newLine = []
    lead = theLineSplit[0]
    label = theLineSplit[1]

    lead = lead.replace(':', '')
    paperNumber = lead[0:3]
    paperType = lead[-1]
#    print('LINE %s' % (theLineSplit))
#    print('NUMBER TYPE %s %s' % (paperNumber, paperType))
#    print('LABEL %s %s' % (paperNumber, label))

    if 'DELETIONS' in label:
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[3],theLineSplit[4]]

    if 'EDITDISTS' in label:
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[3],theLineSplit[4]]

    if 'INSERTBYDIST' in label:
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[3],theLineSplit[4]]

    if 'INSERTIONS' in label:
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[3],theLineSplit[4]]

    if 'SIMILARITY' in label:
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[2], theLineSplit[3],theLineSplit[4]]



    if 'PARACOUNTS' in label:
#        print('zozozozoz %s' % (theLineSplit))
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[2], theLineSplit[3]]
#        print('zozozozoz %s' % (newLine))

    if 'SENTENCECOUNTS' in label:
#        print('zfzfzfzfz %s' % (theLineSplit))
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[2], theLineSplit[3]]
#        print('zfzfzfzfz %s' % (newLine))

    if 'SENTENCELENGTH' in label:
#        print('zfzfzfzfz %s' % (theLineSplit))
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[2]]
#        print('zfzfzfzfz %s' % (newLine))



    if ('ALIGN' in label) and ('COUNT' in label):
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[2], theLineSplit[4], \
                   theLineSplit[5], theLineSplit[6]]
#        print('zyzyzyzyz %s' % (theLineSplit))
#        print('zyzyzyzyz %s' % (newLine))



    if 'EDITDISTFRACTION' in label:
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[4],theLineSplit[5], \
                   theLineSplit[6],theLineSplit[7]]

    if 'SENTENCESBAGS' in label:
        newLine = [label, paperNumber, paperType, \
                   theLineSplit[4],theLineSplit[5], \
                   theLineSplit[6],theLineSplit[7]]
    return newLine

######################################################################
##
def printDict(label, theDict):
    print('\n%s' %(label))
    fout.write('\n%s\n' %(label))
    for key, value in sorted(theDict.items()):
        print('%5d %5d' % (key, value))
        fout.write('%5d %5d\n' % (key, value))
    print('')
    fout.write('\n')

######################################################################
## read the data and return dictionaries of (count, freq) pairs
## including the counts for which the freq is zero
##
##
def readTheData(inFileName):
    theData = defaultdict()
    dataFile = open(inFileName)
    for line in dataFile:
        sent = HistoSentence(line)
        lineSplit = line.split()

#        if '0' == lineSplit[7]:
#            print('TRASH 0 for %s %s' % (lineSplit[1], line))
#            continue

        # ok, here's a hiccup
        # we want both draft and final to sort in order of their
        #      own sentence subs
        if 'DRAFT' == lineSplit[2]:
            key = '%6s %5s %4s %4s' % (lineSplit[1], lineSplit[2], \
                                       lineSplit[7], lineSplit[12])
        elif 'FINAL' == lineSplit[2]:
            key = '%6s %5s %4s %4s' % (lineSplit[1], lineSplit[2], \
                                       lineSplit[12], lineSplit[7])
        else:
            print('ERROR: sentence is neither DRAFT nor FINAL %s' %(sent))
            sys.exit()

        sent.checkInternalCorrectness()

        theData[key] = sent

    oldkey = 'A B C D'
    oldkeysplit = oldkey.split()
    for key, value in sorted(theData.items()):
        keysplit = key.split()
        print('FOR TRASHING %s %s' % (keysplit, value))

        if ('DRAFT' == keysplit[1]) and ('FINAL' == oldkeysplit[1]):
            print('YES TRASH FINAL TO DRAFT %s' % (oldkeysplit))
            del theData[oldkey]
        if ('FINAL' == keysplit[1]) and ('DRAFT' == oldkeysplit[1]):
            print('YES TRASH DRAFT TO FINAL %s' % (oldkeysplit))
            del theData[oldkey]

        if '0' == keysplit[2]:
            if '0' == keysplit[3]:
                print('YES TRASH ZERO %s' % (keysplit))
                del theData[key]
            else:
                print('ERROR TRASH ZERO %s %s' % (keysplit, value))
                sys.exit()

        oldkey = key
        oldkeysplit = keysplit

    print('YES TRASH LAST ENTRY %s' % (oldkeysplit))
    del theData[oldkey] # don't forget the last one

    return theData

######################################################################
## do the scatter plots of edit distance fractions against bags
def scatterplot(theData, whichEvent, fileName):

    xCoords = []
    yCoordsDraft = []
    yCoordsFinal = []

    for line in theData:
        if whichEvent not in line[0]: continue
        xCoords.append(line[3])
        yCoordsDraft.append(line[4])
        yCoordsFinal.append(line[5])

    plt.scatter(xCoords, yCoordsDraft)
    plt.xlabel('Plot (draft) ' + whichEvent)
    plt.savefig(fileName + 'Draft')
#    plt.show()
    plt.clf()
    plt.cla()

    plt.scatter(xCoords, yCoordsFinal)
    plt.xlabel('Plot (final) ' + whichEvent)
    plt.savefig(fileName + 'Final')
#    plt.show()
    plt.clf()
    plt.cla()

    plt.scatter(yCoordsDraft, yCoordsFinal)
    plt.xlabel('Plot draft bag against final bag ' + whichEvent)
    plt.savefig(fileName + 'BagsDraftAgainstFinal')
#    plt.show()

######################################################################
## do the scatter plots of edit distance fractions against bags
def scatterplotB(theData, whichEvent, fileName):
#    import numpy as np
#    import matplotlib.pyplot as plt

    xCoords = []
    yCoords5 = []
    yCoords6 = []

    for line in theData:
        if whichEvent not in line[0]: continue
        xCoords.append(line[3])
        yCoords5.append(line[5])
        yCoords6.append(line[6])

#    print('SCATTERA ', xCoords)
#    print('SCATTERB ', yCoords5)
    plt.scatter(xCoords, yCoords5)
#    print('SCATTERC ')
    plt.xlabel('Plot (draft) ' + whichEvent)
    plt.savefig(fileName + 'Draft')
#    plt.show()
#    print('SCATTERD ')

#    print('SCATTERE ', xCoords)
#    print('SCATTERF ', yCoords5)
    plt.scatter(xCoords, yCoords6)
#    print('SCATTERG ')
    plt.xlabel('Plot (final) ' + whichEvent)
    plt.savefig(fileName + 'Final')
#    plt.show()
#    print('SCATTERH ')

######################################################################
## MAIN PROGRAM STARTS HERE
##
checkArgs(3, "usage: a.out inFileName outFileName")

TAG = 'FYEHISTO:'

inFileName = sys.argv[1]
outFileName = sys.argv[2]

if 'stdout' == outFileName:
    fout = sys.stdout
else:
    fout = open(outFileName, 'w')

print("%s INFILE='%s' OUTFILE='%s'" % (TAG, inFileName, outFileName))
fout.write("%s INFILE='%s' OUTFILE='%s'\n" % (TAG, inFileName, outFileName))

# first we have to read the data
theData = readTheData(inFileName)

# and we check that what we have read makes sense
for key, value in sorted(theData.items()):
#    print('KEYVALUE %22s %s' % (key, value))
    thisSent = value
    if thisSent.isAligned():
        keySplit = key.split()
        if keySplit[3] != ALIGNMENTDUMMYSUB:
            if 'DRAFT' == keySplit[1]:
                keyLabel = 'FINAL'
            else:
                keyLabel = 'DRAFT'
            alignedSentKey = '%6s %5s %4s %4s' % (keySplit[0], keyLabel, \
                                                  keySplit[3], keySplit[2])
            alignedSent = theData[alignedSentKey]
            thisSent.checkAlignedSentences(alignedSent)

######################################################################
##
maxRangeForType = 5

listOfFilters = ['ALL']

localData = defaultdict()
lastParaNumDict = defaultdict(int)
for filter in listOfFilters:

    # create the local data dict, and while we are at it, find
    # the last para number for each document
    for key, value in sorted(theData.items()):
        localData[key] = value
        keysplit = key.split()
        if 'DRAFT' == keysplit[1]:
            lastParaNumDict[key.split()[0]+' '+key.split()[1]] = value.getLeftParaSub()
        elif 'FINAL' == keysplit[1]:
            lastParaNumDict[key.split()[0]+' '+key.split()[1]] = value.getRightParaSub()

#    fout.write('LAST PARA NUM SIZE %4d\n' % (len(lastParaNumDict)))
#    for key, value in lastParaNumDict.items():
#        fout.write('LAST PARA NUM %s %4d\n' % (key, value))

    for theType in range(0, maxRangeForType):
        histoEditDistance(localData, theType, 'DRAFT', lastParaNumDict, 'ALL', fout)
        histoEditDistance(localData, theType, 'DRAFT', lastParaNumDict, 'FIRST', fout)
        histoEditDistance(localData, theType, 'DRAFT', lastParaNumDict, 'MIDDLE', fout)
        histoEditDistance(localData, theType, 'DRAFT', lastParaNumDict, 'LAST', fout)
        histoEditDistance(localData, theType, 'FINAL', lastParaNumDict, 'ALL', fout)
        histoEditDistance(localData, theType, 'FINAL', lastParaNumDict, 'FIRST', fout)
        histoEditDistance(localData, theType, 'FINAL', lastParaNumDict, 'MIDDLE', fout)
        histoEditDistance(localData, theType, 'FINAL', lastParaNumDict, 'LAST', fout)

    for theType in range(0, maxRangeForType):
        histoDeletionsByPara(localData, theType, 'DRAFT', lastParaNumDict, 'ALL', fout)
        histoDeletionsByPara(localData, theType, 'DRAFT', lastParaNumDict, 'FIRST', fout)
        histoDeletionsByPara(localData, theType, 'DRAFT', lastParaNumDict, 'MIDDLE', fout)
        histoDeletionsByPara(localData, theType, 'DRAFT', lastParaNumDict, 'LAST', fout)

    for theType in range(0, maxRangeForType):
        histoInsertionsByPara(localData, theType, 'FINAL', lastParaNumDict, 'ALL', fout)
        histoInsertionsByPara(localData, theType, 'FINAL', lastParaNumDict, 'FIRST', fout)
        histoInsertionsByPara(localData, theType, 'FINAL', lastParaNumDict, 'MIDDLE', fout)
        histoInsertionsByPara(localData, theType, 'FINAL', lastParaNumDict, 'LAST', fout)

    for theType in range(0, maxRangeForType):
        histoInsertionsByEditDistFrac(localData, theType, 'FINAL', fout)

    for theType in range(0, maxRangeForType):
        histoParagraphCounts(localData, theType, 'DRAFT', fout)
        histoParagraphCounts(localData, theType, 'FINAL', fout)

    for theType in range(0, maxRangeForType):
        histoSentenceCounts(localData, theType, 'DRAFT', fout)
        histoSentenceCounts(localData, theType, 'FINAL', fout)

    for theType in range(0, maxRangeForType):
        histoWordCounts(localData, theType, 'DRAFT', fout)
        histoWordCounts(localData, theType, 'FINAL', fout)

#for theType in range(0, maxRangeForType):
#    histoSentenceLengthCounts(theData, theType, 'DRAFT')
#    histoSentenceLengthCounts(theData, theType, 'FINAL')

    for theType in range(0, maxRangeForType):
        histoAlignmentLevels(localData, theType, 'DRAFT', fout)

    for theType in range(0, maxRangeForType):
        histoAlignmentFractionsByLevel(localData, theType, 'DRAFT', fout)
        histoAlignmentFractionsByLevel(localData, theType, 'FINAL', fout)

#sys.exit()

#scatterplot(theData, 'SIMILARITY', 'EditDistFrac')

sys.exit()
