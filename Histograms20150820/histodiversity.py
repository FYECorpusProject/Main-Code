#!/usr/bin/env python ## use python 2.7

import sys
from collections import defaultdict
from os import listdir
from histogramcode import Histogram
from histosentence import HistoSentence
##
import numpy as np
import matplotlib.pyplot as plt

######################################################################
## FUNCTIONS

######################################################################
## check arguments
def checkArgs(number, message):
    if len(sys.argv) != number:
        print(message)
        sys.exit(1)

######################################################################
## histogram of lexical diversity
def histoDiversity(theData, theType, outFile):
    draftDict = defaultdict(int)
    finalDict = defaultdict(int)

    for line in theData:
        name = line[1]
        if (0 != theType) and (int(theType) != int(name[-1])): continue
        draftDiversity = float(line[4]) / float(line[3])
        finalDiversity = float(line[6]) / float(line[5])
        draftRounded = round(100 * draftDiversity)
        finalRounded = round(100 * finalDiversity)
        draftDict[int(draftRounded)] += 1
        finalDict[int(finalRounded)] += 1
#        print('%s %s %s %3d %3d' % \
#              (name, name[-1], theType, int(draftRounded), (finalRounded) ))
        

    which = 'DRAFT'
    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo = 'Diversity is quotient of #uniq words and #words for ' + which + '\n'
    headerInfo += 'Column 1: This quotient times 100\n'
    headerInfo += 'Column 2: Percent of papers with this quotient\n'
    headerInfo += 'Column 3: Raw number of papers with this quotient\n'
    headerInfo += 'Column 4: The histogram\n'
    label = 'DIVERSITY FOR TYPE %d\n' % (theType)
    label += headerInfo

    if len(draftDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, draftDict, 1, 1, outFile)
        outFile.write('%s\n' % (histo))
    else:
#        print('NO PAPERS FOR %s\n' % (label))
        outFile.write('NO PAPERS FOR %s\n' % (label))

    which = 'FINAL'
    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo = 'Diversity is quotient of #uniq words and #words for ' + which + '\n'
    headerInfo += 'Column 1: This quotient times 100\n'
    headerInfo += 'Column 2: Percent of papers with this quotient\n'
    headerInfo += 'Column 3: Raw number of papers with this quotient\n'
    headerInfo += 'Column 4: The histogram\n'
    label = 'DIVERSITY FOR TYPE %d\n' % (theType)
    label += headerInfo

    if len(finalDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, finalDict, 1, 1, outFile)
        outFile.write('%s\n' % (histo))
    else:
#        print('NO PAPERS FOR %s\n' % (label))
        outFile.write('NO PAPERS FOR %s\n' % (label))

######################################################################
## histogram of lexical diversity by word count
def histoDiversityByWordCount(theData, theType, whichLeft, whichRight, outFile):
    allDict = defaultdict(int)
    nonstopDict = defaultdict(int)

    ######################################################################
    ## REMEMBER that general diversity is all and nonstopwords
    ## REMEMBER that student diversity is all for draft and final
    ALLDIVERSITY = 6
    NONSTOPDIVERSITY = 9
    #ALLDIVERSITY = 5
    #NONSTOPDIVERSITY = 8

    allRoundedList = []
    nonstopRoundedList = []
    for line in theData:
        name = line[1]
        name = name.replace('.txt', '')
        if (0 != theType) and (int(theType) != int(name[-1])): continue
        allDiversity = float(line[ALLDIVERSITY])
        nonstopDiversity = float(line[NONSTOPDIVERSITY])
        allRounded = round(100 * allDiversity)
        allRoundedList.append(allRounded)
        nonstopRounded = round(100 * nonstopDiversity)
        nonstopRoundedList.append(nonstopRounded)
        allDict[int(allRounded)] += 1
        nonstopDict[int(nonstopRounded)] += 1
#        print('%s %s %s %3d %3d' % \
#              (name, name[-1], theType, int(draftRounded), (finalRounded) ))
        

#    which = 'ALL'
    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo = 'Diversity is quotient of #uniq words and #words for ' + whichLeft + '\n'
    headerInfo += 'Column 1: This quotient times 100\n'
    headerInfo += 'Column 2: Percent of papers with this quotient\n'
    headerInfo += 'Column 3: Raw number of papers with this quotient\n'
    headerInfo += 'Column 4: The histogram\n'
    label = 'DIVERSITY FOR TYPE %d\n' % (theType)
    label += headerInfo

    if len(allDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, allDict, 1, 1, outFile)
        outFile.write('%s\n' % (histo))
    else:
#        print('NO PAPERS FOR %s\n' % (label))
        outFile.write('NO PAPERS FOR %s\n' % (label))

#    which = 'NONSTOP'
    headerInfo = '\nInput from file: %s\n' % (inFileName)
    headerInfo = 'Diversity is quotient of #uniq words and #words for ' + whichRight + '\n'
    headerInfo += 'Column 1: This quotient times 100\n'
    headerInfo += 'Column 2: Percent of papers with this quotient\n'
    headerInfo += 'Column 3: Raw number of papers with this quotient\n'
    headerInfo += 'Column 4: The histogram\n'
    label = 'DIVERSITY FOR TYPE %d\n' % (theType)
    label += headerInfo

    if len(nonstopDict) > 0:
        histo, shortVersion = Histogram.histoTheData(label, nonstopDict, 1, 1, outFile)
        outFile.write('%s\n' % (histo))
    else:
#        print('NO PAPERS FOR %s\n' % (label))
        outFile.write('NO PAPERS FOR %s\n' % (label))

    print(allRoundedList)

    if len(allRoundedList) > 0:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        numBins = 50
#        ax.hist(allRoundedList,numBins,color='green',alpha=0.8)
#        ax.hist(nonstopRoundedList,numBins,color='red',alpha=0.8)
#        plt.show()

        multiset = [allRoundedList, nonstopRoundedList]
        ax.hist(multiset, numBins, color=['green','red'],label = ['All', 'Nonstop'], alpha=0.8)
        ax.legend(prop={'size': 10})
        ax.set_title('Allword versus Nonstopword diversity')
        plt.show()


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
def readTheData(inFileName):
    theData = []
    dataFile = open(inFileName)
    for line in dataFile:
        lineSplit = line.split()

        theData.append(lineSplit)

    return theData

######################################################################
## do the scatter plots of edit distance fractions against bags
def scatterplot(theData, xsub, ysub, fileName):

    xCoords = []
    yCoords= []

    for line in theData:
        xCoords.append(line[xsub])
        yCoords.append(line[ysub])

    plt.scatter(xCoords, yCoords, color='r')
    plt.xlabel('Plot Diversity')
    plt.savefig(fileName)
#    plt.show()
    plt.clf()
    plt.cla()

#    plt.show()

######################################################################
## MAIN PROGRAM STARTS HERE
##
checkArgs(4, "usage: a.out bookDiversityFileName inFileName outFileName")

TAG = 'DIVERSITY:'

bookDiversityFileName = sys.argv[1]
inFileName = sys.argv[2]
outFileName = sys.argv[3]

if 'stdout' == outFileName:
    fout = sys.stdout
else:
    fout = open(outFileName, 'w')

print("%s INFILE='%s' OUTFILE='%s'" % (TAG, inFileName, outFileName))
fout.write("%s INFILE='%s' OUTFILE='%s'\n" % (TAG, inFileName, outFileName))

# first we have to read the data
theBook = readTheData(bookDiversityFileName)
theData = readTheData(inFileName)

#for line in theData:
#    print(line)

######################################################################
## plot
######################################################################
## REMEMBER that general diversity is all and nonstopwords
## REMEMBER that student diversity is all for draft and final
#scatterplot(theData, 5, 8, 'Zork')
scatterplot(theBook, 6, 9, 'AllVsNonstop')
scatterplot(theData, 6, 9, 'Student')

######################################################################
## diversity
maxRangeForType = 5

for theType in range(0, maxRangeForType):
    histoDiversityByWordCount(theData, theType, 'DRAFT', 'FINAL', fout)
    histoDiversityByWordCount(theBook, theType, 'ALL', 'NONSTOP', fout)

#print(theData)

### histogramplot test
#fig = plt.figure()
#ax = fig.add_subplot(111)
#
#x = np.random.normal(0,1,1000)
#numBins = 50
#ax.hist(x,numBins,color='green',alpha=0.8)
#plt.show()

sys.exit()
