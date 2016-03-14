from collections import defaultdict
import nltk
import sys
import time
import subprocess as SP
from os import listdir
from operator import itemgetter
from operator import attrgetter

from constants import *
from dabfunctions import checkArgs
from dabfunctions import printoutput
from editdistance import EditDistance
from mytimer import MyTimer
from returnedvalues import ReturnedValues
from sentence import Sentence
from profiler import LinguisticProfiler

######################################################################
## FUNCTIONS

#######################################################################
### align the stanford tagged sentences with the corpus sentences
#def alignStanfordWithCorpus(doc, taggedlines, taggedlineswithouttags):
#    sentencelist = []
#    corpusparasub = -1 
#    corpussentencesub = -1 
#    stanfordsentencesub = -1 
#    for corpuspara in doc.paras():
#        corpusparasub += 1 
##        print(corpuspara)
#        for corpussent in corpuspara:
#            corpussentencesub += 1 
#            stanfordsentencesub += 1 
#            stanfordsent = taggedlineswithouttags[stanfordsentencesub]
#            if matchStanfordWithCorpus(corpussent, stanfordsent):
#                print('\nMATCH %3d %3d' % (corpusparasub, corpussentencesub))
#                print('MATCH CORPUS   %s' % (corpussent))
#                print('MATCH STANFORD %s' % (stanfordsent))
#                sentencelist.append([corpusparasub, corpussentencesub, \
#                                     corpussent, stanfordsent, \
#                                taggedlines[stanfordsentencesub]])
##                outstring = '%s %s LIST: %3d: %s' % (TAG, idnumber, \
##                                                     corpussentencesub, \
##                                                     corpussent)
##                printoutput(outstring, outfile)
#            else:
#                print('\nNOMATCH %3d %3d' % (corpusparasub, corpussentencesub))
#                print('NOMATCH   %s' % (corpussent))
#                print('NOMATCH   %s' % (stanfordsent))
#                print('NOMATCH   %s' % (taggedlines[stanfordsentencesub]))
#                sys.exit()
#
#    return sentencelist

######################################################################
## do the computation for bags of words 
def bagComputation(leftsentence, rightsentence):
    bagsizevalueleft = 0.0
    bagSizeValueFinal = 0.0
#    bagDraft = leftSent.createBagOfWords()
#    bagFinal = rightSent.createBagOfWords()
    bagleft = leftsentence.getbagofwords()
    bagright = rightsentence.getbagofwords()
    lenleft = len(bagleft)
    lenright = len(bagright)

    lenintersection = len(bagleft.intersection(bagright))
    if lenleft > 0:
        bagsizevalueleft = float(lenintersection)/float(lenleft)
    else:
        bagsizevalueleft = 1.0

    leftsentence.setbagsizefrac(bagsizevalueleft)

    if lenright > 0:
        bagsizevalueright = float(lenintersection)/float(lenright)
    else:
        bagsizevalueright = 1.0

    rightsentence.setbagsizefrac(bagsizevalueright)

    outputLine = ' bagsizes %3d %3d %3d %5.2f %5.2f' % \
        (lenleft, lenright, lenintersection, \
         bagsizevalueleft, bagsizevalueright)

    return bagsizevalueleft, bagsizevalueright, outputLine

######################################################################
## build a list of strings for side by side display
def buildStringList(LINELENGTH, sentence):
    s = ''
    theList = []
    for word in sentence:
        if len(s) + len(word) < LINELENGTH:
            s = s + ' ' + word
        else:
            s = s.strip()
            theList.append(s)
            s = word
    if len(s) > 0:
        s = s.strip()
        theList.append(s)
    return theList

#######################################################################
### clean a single sentence of capital letters, punctuation, and such
#def cleanSentenceUp(sent):
#    newSent = []
#    for word in sent.getsent():
##        word = word.replace('\x80', ' ')
##        word = word.replace('\x94', ' ')
##        word = word.replace('\x98', ' ')
##        word = word.replace('\x99', ' ')
##        word = word.replace('\x9c', ' ')
##        word = word.replace('\xe2', ' ')
##        word = word.replace('\xe2', ' ')
##        word = word.replace('\xe4', ' ')
#
#        if skipthisword(word): continue
#
#        word = word.lower()
#        word = word.strip()
#        if len(word) > 0:
#            newSent.append(word)
#
#        lastSentenceFinal = Sentence(name, 'FINAL', numpara-1, \
#                            overallnumsent, \
#                            ['inserted', 'last', 'sentence'], \
#                            ['inserted_VBN', 'last_JJ', 'sentence_NN'], \
#                            stopwords)
#
#    return newSent

#######################################################################
### clean the sentences of capital letters and punctuation and such
##def cleanSentencesUp(sents):
#    newSentences = []
##    for sent in sents:
##        newSent = []
##        for word in sent:
###            word = word.replace('\x80', ' ')
###            word = word.replace('\x94', ' ')
###            word = word.replace('\x98', ' ')
###            word = word.replace('\x99', ' ')
###            word = word.replace('\xe2', ' ')
###            word = word.replace('\xe2', ' ')
###            word = word.replace('\xe4', ' ')
##
##            if skipthisword(word): continue
##
##            word = word.lower()
##            word = word.strip()
##            if len(word) > 0:
##                newSent.append(word)
##
##        ## skip over a sentence that is only the word 'chapter'
##        if (1 == len(newSent)) and ('chapter' == newSent[0]):
##            continue
##
##        if len(newSent) > 0:
##            newSentences.append(newSent)
##
##    return newSentences

######################################################################
## compute the fraction of worst case edit distance that we have 
def computeWorstCaseFrac(leftSent, rightSent, distance):
#    print('%s %s %d\n' % (leftSent, rightSent, distance))
    leftLen = leftSent.getlength()
    rightLen = rightSent.getlength()

    if 0 == leftLen + rightLen:
        worstCaseFrac = 0.0
    else:
        worstCaseFrac = float(distance)/(float(leftLen) + float(rightLen))

    return worstCaseFrac

#######################################################################
### create a file that has its characters cleaned for utf-8 and ascii
#def createCharacterCleanedFile(TAG, pathtodata, name):
#    filename = pathtodata + '/' + name
##    print('open file %s' % (filename))
#    outstring = '%s open file %s' % (TAG, filename)
#    printoutput(outstring, outfile)
##    theFile = open(filename) # old version
#    theFile = open(filename, encoding='ISO-8859-2') # python 3
##    theFile = open(filename) # python 2.7
#    theText = theFile.read()
#
#    theText = theText.replace('\x85', '...') # ellipsis
#    theText = theText.replace('\x91', "'") # smart open single quote
#    theText = theText.replace('\x92', "'") # smart close single quote
#    theText = theText.replace('\x93', '"') # smart open quote
#    theText = theText.replace('\x94', '"') # smart close quote
#    theText = theText.replace('\x96', '-') # short dash
#    theText = theText.replace('\x97', '--') # long dash
#    theText = theText.replace('\x9c', '"') # smart close quote
#    theText = theText.replace('\x9d', '"') # smart close quote
#    theText = theText.replace('\xa0', ' ') # not sure
#    theText = theText.replace('\xac', ' ') # not sure
#    theText = theText.replace('\xb4', ' ') # not sure
#    theText = theText.replace('\xb8', ' ') # not sure
#    theText = theText.replace('\xb9', ' ') # not sure
#    theText = theText.replace('\xe4', 'ae') # a umlaut
#    theText = theText.replace('\xe7', 'c') # cedilla
#    theText = theText.replace('\xe9', 'e') # e acute
#    theText = theText.replace('\xe1', ' ') # not sure
#    theText = theText.replace('\xe3', ' ') # not sure
#    theText = theText.replace('\xef', 'i') # i with diaresis
#    theText = theText.replace('\xfe', ' ') # not sure
#    theText = theText.replace('\xff', ' ') # not sure
#
#    theText = theText.replace('\x80', ' ')
#    theText = theText.replace('\x88', ' ')
#    theText = theText.replace('\x8c', ' ')
#    theText = theText.replace('\x8d', ' ')
#    theText = theText.replace('\x94', ' ')
#    theText = theText.replace('\x95', ' ')
#    theText = theText.replace('\x98', ' ')
#    theText = theText.replace('\x99', ' ')
#    theText = theText.replace('\xa9', ' ')
#    theText = theText.replace('\xc4', ' ')
#    theText = theText.replace('\xe2', ' ')
#    theText = theText.replace('\xe2', ' ')
#    theText = theText.replace('\xe4', ' ')
#
#    theText = theText.replace('."', '".') # is this right or necessary?
#
#    theText = theText.replace('(', '') # ntlk takes these as separate sentences
#    theText = theText.replace(')', '')
#
## added 19 January 2015 to try to remove sentences of zero length
##    theText = theText.strip()
#
#    theText = 'inserted first sentence. ' + theText
#    theText = theText + ' inserted last sentence.'
#
#    theOutput = open('zzzztemp'+name, 'w')
#    theOutput.write('%s' % (theText))
#    theOutput.close()
##    print(theText)

######################################################################
## display the aligned list 
def displayAligned(label, name, matchList, sents1, sents2, level, outfile, \
                   distanceMatrix, ALIGNMAX, BAGMIN, printit=False):

# note the way we are walking this list
    outstring = '\n%s %s' % (name, label)
    printoutput(outstring, outfile)
    label = label.split()[0]
    midList = []
    for i in range(0, len(matchList)):
        itemCurrent = matchList[i]
        sub1Current = itemCurrent[0]
        sub2Current = itemCurrent[1]
        distCurrent = itemCurrent[2]
        if printit:
            displaySideBySide(label, name, distCurrent, sub1Current, sub2Current, \
                              sents1[sub1Current], sents2[sub2Current], \
                              'v', '^', outfile)
        outstring = ''
        printoutput(outstring, outfile)
        if i < len(matchList)-1:
            itemNext = matchList[i+1]
            sub1Next = itemNext[0]
            sub2Next = itemNext[1]
            distNext = itemNext[2]
        else:
            distNext = DUMMY
            sub1Next = sub1Current
            sub2Next = sub2Current

        line1 = sents1[sub1Current].formatsub(sub1Current)
        line2 = sents2[sub2Current].formatsub(sub2Current)
        outstring = '%s CURRENTALIGN %5s = %5s' % (name, line1, line2)
        printoutput(outstring, outfile)

        line1 = sents1[sub1Next].formatsub(sub1Next)
        line2 = sents2[sub2Next].formatsub(sub2Next)
        outstring = '%s NEXTALIGN    %5s = %5s' % (name, line1, line2)
        printoutput(outstring, outfile)

        begin1 = sub1Current + 1
        begin2 = sub2Current + 1
        end1 = sub1Next - 1
        end2 = sub2Next - 1
        outoutstring = ''
        if (begin1 < len(sents1)) and (end1 < len(sents1)) and \
           (begin2 < len(sents2)) and (end2 < len(sents2)):

            outstring = '%s TEST RANGES (LEFT FROM %5s THROUGH %5s) (RIGHT FROM %5s THROUGH %5s)' % \
                  (name, sents1[begin1].formatsub(begin1), \
                         sents1[end1].formatsub(end1), \
                         sents2[begin2].formatsub(begin2), \
                         sents2[end2].formatsub(end2))

#        displaySubmatrix(begin1, end1, begin2, end2, distanceMatrix)

#            minDist, rowMin, colMin = findMin(begin1, end1, sents1, \
            minList = findMinFrac(begin1, end1, sents1, \
                                  begin2, end2, sents2, \
                                  distanceMatrix, DUMMY)
            minA = minList[0]
            minB = minList[1]
            minC = minList[2]

            minDist = minA[0]
            minFrac = minA[1]
            rowMin = minA[2]
            colMin = minA[3]
            outoutstring = '\n%3d %6.3f %3d %3d' % \
                           (minDist, minFrac, rowMin, colMin)

            newMinDistDel = minB[0]
            newMinFracDel = minB[1]
            newMinRowDel = minB[2]
            newMinColDel = minB[3]
            outoutstring += '\n%3d %6.3f %3d %3d' % \
                           (newMinDistDel, newMinFracDel, newMinRowDel, newMinColDel)
            if newMinRowDel != rowMin: outoutstring += ' ZORKROWDEL'
            if newMinColDel != colMin: outoutstring += ' ZORKCOLDEL'

            newMinDistIns = minC[0]
            newMinFracIns = minC[1]
            newMinRowIns = minC[2]
            newMinColIns = minC[3]
            outoutstring += '\n%3d %6.3f %3d %3d' % \
                           (newMinDistIns, newMinFracIns, newMinRowIns, newMinColIns)
            if newMinRowIns != rowMin: outoutstring += ' ZORKROWINS'
            if newMinColIns != colMin: outoutstring += ' ZORKCOLINS'
            outoutstring += '\n'

        else:
            outstring = '%s TEST RANGES OUT OF BOUNDS %3d-->%3d %3d-->%3d' % \
                         (name, begin1, end1, begin2, end2)
            minDist = DUMMY

        printoutput(outstring, outfile)
        printoutput(outoutstring, outfile)

        if DUMMY == minDist:
            outstring = '%s NOTHING IN BETWEEN' % (name)
            printoutput(outstring, outfile)
        else:
            displaySubmatrix(name, begin1, end1, begin2, end2, distanceMatrix)
            outstring = '%s MIN AND MINFRAC %4d %10.3f AT (%4d <--> %4d)\n' % \
                           (name, minDist, minFrac, rowMin, colMin)
            printoutput(outstring, outfile)

            worstCaseFrac = computeWorstCaseFrac(sents1[rowMin], \
                                                 sents2[colMin], \
                                                 minDist)
#alignOutLine = '       %3d %3d %3d' % (leftLen, rightLen, leftLen+rightLen)

            bagSizeValueDraft, bagSizeValueFinal, outputLine = \
                   bagComputation(sents1[rowMin], sents2[colMin])
            outstring = '%s ALIGN AND BAG %4d<-->%4d        %3d %3d %3d %5.3f ' % \
                           (name, rowMin, colMin, \
                            sents1[rowMin].getlength(), \
                            sents2[colMin].getlength(), \
                      sents1[rowMin].getlength()+sents2[colMin].getlength(), \
                            worstCaseFrac)

            outstring += '%s %5.2f %5.2f\n' % \
                          (outputLine, bagSizeValueDraft, bagSizeValueFinal)
            outstring += '\n%d %s\n%d %s' % (rowMin, sents1[rowMin], colMin, sents2[colMin])
            printoutput(outstring, outfile)

#zork
#            newDel, newIns = dogapcomputation(sents1[rowMin], sents2[colMin])
#            if newDel != distanceMatrix[rowMin][colMin][1]:
#                print('ERROR (%d %d) %d %d %s' % (rowMin, colMin, newDel, newIns, distanceMatrix[rowMin][colMin]))
#            else:
#                print('GOOD DEL (%d %d)' % (rowMin, colMin))
#            if newIns != distanceMatrix[rowMin][colMin][2]:
#                print('ERROR (%d %d) %d %d %s' % (rowMin, colMin, newDel, newIns, distanceMatrix[rowMin][colMin]))
#            else:
#                print('GOOD INS (%d %d)' % (rowMin, colMin))

            if (worstCaseFrac <= ALIGNMAX) and (bagSizeValueDraft >= BAGMIN):
                outstring = '%s YES WE ALIGN THESE SENTENCES' % (name)
                printoutput(outstring, outfile)

                midList.append([rowMin, colMin, minDist, level])
#                print('SETALIGNC %d %d %d' % (rowMin, colMin, level))
                sents1[rowMin].setalignment(level, sents2[colMin], minDist)
                sents2[colMin].setalignment(level, sents1[rowMin], minDist)
            else:
                if worstCaseFrac > ALIGNMAX:
                    outstring = '%s WORSTCASEFRACTION TOO LARGE\n' % (name)
                elif bagSizeValueDraft < BAGMIN:
                    outstring = '%s BAGSIZEVALUE TOO SMALL\n' % (name)

                printoutput(outstring, outfile)

        counter = 0
        while (counter+begin1 <= end1) or (counter+begin2 <= end2):

            if counter+begin1 <= end1:
                sentence1 = sents1[counter+begin1]
                leftSub = counter+begin1
            else:
#                sentence1 = Sentence(name, 'DRAFT', DUMMY, DUMMY, [' '], stopwords)
                sentence1 = Sentence(name, 'DRAFT', DUMMY, DUMMY, \
                                     [' '], [' '], stopwords)
                leftSub = DUMMY

            if counter+begin2 <= end2:
                sentence2 = sents2[counter+begin2]
                rightSub = counter+begin2
            else:
#                sentence2 = Sentence(name, 'FINAL', DUMMY, DUMMY, [' '], stopwords)
                sentence2 = Sentence(name, 'DRAFT', DUMMY, DUMMY, \
                                     [' '], [' '], stopwords)
                rightSub = DUMMY

            if printit:
                displaySideBySide(label, name, ALIGNMENTDUMMYSUB, leftSub, rightSub, \
                                  sentence1, sentence2, '-', '-', outfile)

            counter += 1

    return midList
    
######################################################################
## display sentences side by side
def displaySideBySide(label, name, dist, sub1, sub2, sent1, sent2, \
                      upper, lower, outfile):
    LINELENGTH = 60

    s = '                  '
    for i in range(0, 2*LINELENGTH // 5):
        s += upper + '    '
#    outfile.write('%s %s %s\n' % (name, label, s))
    outstring = '%s %s %s' % (name, label, s)
    printoutput(outstring, outfile)

    filefmt = '%%-%ds  ****  %%-%ds' % (LINELENGTH, LINELENGTH)
    filefmt1 = '%s %s %3d (%5s %5s) ' + filefmt
    filefmt1a = '%s %s XXX (      %5s) ' + filefmt
    filefmt1b = '%s %s XXX (%5s      ) ' + filefmt
    filefmt2 = '%s %s                   ' + filefmt
    # build the lists of strings for the sentences
    list1 = buildStringList(LINELENGTH, sent1.getsent())
    list2 = buildStringList(LINELENGTH, sent2.getsent())

    maxLen = len(list1)
    if len(list2) > maxLen: maxLen = len(list2)

    block1 = []
    block2 = []
    for i in range(0, maxLen):
        block1.append(' ')
        block2.append(' ')

    for i in range(0, len(list1)):
        block1[i] = list1[i]

    for i in range(0, len(list2)):
        block2[i] = list2[i]

    for i in range(0, maxLen):
        if 0 == i:
            if sub1 == DUMMY:
                outstring = filefmt1a % (name, label, \
                                         sent2.formatsub(sub2), \
                                         block1[i], block2[i])
                printoutput(outstring, outfile)
            elif sub2 == DUMMY:
                outstring = filefmt1b % (name, label, \
                                         sent1.formatsub(sub1), \
                                         block1[i], block2[i])
                printoutput(outstring, outfile)
            else:
                outstring = filefmt1 % (name, label, dist, \
                                        sent1.formatsub(sub1), \
                                        sent2.formatsub(sub2), \
                                        block1[i], block2[i])
                printoutput(outstring, outfile)
        else:
            outstring = filefmt2 % (name, label, block1[i], block2[i])
            printoutput(outstring, outfile)

    s = '                  '
    for i in range(0, 2*LINELENGTH // 5):
        s += lower + '    '
    outstring = '%s %s %s' % (name, label, s)
    printoutput(outstring, outfile)

######################################################################
## display a submatrix
## NOTE THAT THE ENDING SUBSCRIPTS ARE INCLUSIVE!!!!
def displaySubmatrix(name, begin1, end1, begin2, end2, matrix):
    # header
    s = '%s     :  ' % (name)
    for j in range(begin2, end2+1):
        s += '%11d   ' % (j)
    outstring = '%s' % (s)
    printoutput(outstring, outfile)

    for i in range(begin1, end1+1):
        s = '%s %3d :' % (name, i)
        for j in range(begin2, end2+1):
            s += ' [%3d,%3d,%3d]' % (matrix[i][j][0], matrix[i][j][1], \
                                     matrix[i][j][2])
        outstring = '%s' % (s)
        printoutput(outstring, outfile)

#########################################################################
##### do the gap computation between two sentences
###def dogapcomputation(s1, s2):
###    outstring = 'MAIN: DRAFT %s' % (s1.getsent())
###    printoutput(outstring, outfile)
###    outstring = 'MAIN: FINAL %s' % (s2.getsent())
###    printoutput(outstring, outfile)
###
###    editInstance = EditDistance(s1, s2)
###    distanceList = editInstance.computedistance(outfile)
###    distance = distanceList[0]
###    maxColDel = distanceList[1]
###    maxRowIns = distanceList[2]
###
####    editInstance.display2(outfile)
###    backtracklist = editInstance.backtrack()
####    outstring = 'BACKTRACK %s' % (backtracklist)
####    printoutput(outstring, outfile)
###
###    # find the row insert/delete instances
###    maxrowcount = 0
###    maxcolcount = 0
###    # prepend a dummy to start off the computation
###    alignedpairs = [[[0, 0, 0], [0, 0, 0]]]
###    for listsub in range(0, len(backtracklist)-1): 
###        thiselt = backtracklist[listsub]
###        thisrow = thiselt[0]
###        thiscol = thiselt[1]
###        thisval = thiselt[2]
###
###        nextelt = backtracklist[listsub+1]
###        nextrow = nextelt[0]
###        nextcol = nextelt[1]
###        nextval = nextelt[2]
###
###        if (thisrow != nextrow) and \
###           (thiscol != nextcol) and \
###           (thisval == nextval):
###            alignedpairs.append([thiselt, nextelt])
###
###    alignedpairs.append([nextelt, [nextrow+1, nextcol+1, nextval]])
###    outstring = 'MAIN: ALIGNED   %s' % (alignedpairs)
###    printoutput(outstring, outfile)
###
####    for item in alignedpairs:
####        outstring = '%s %s' % (formatTriple(item[0]), formatTriple(item[1]))
####        printoutput(outstring, outfile)
####    outstring = ''
####    printoutput(outstring, outfile)
###
###    maxColDel = 0
###    maxRowIns = 0
###    for listsub in range(0, len(alignedpairs)-1): 
###        thiselt = alignedpairs[listsub]
###        leftedge = thiselt[1]
###        leftrow = leftedge[0]
###        leftcol = leftedge[1]
###        leftval = leftedge[2]
###
###        nextelt = alignedpairs[listsub+1]
###        rightedge = nextelt[0]
###        rightrow = rightedge[0]
###        rightcol = rightedge[1]
###        rightval = rightedge[2]
###
###        change = rightval - leftval
###
###        if (leftrow != rightrow) and (leftcol != rightcol):
####            outstring = '%s %s CHANGE BOTH %3d' % (formatTriple(leftedge), \
####                                             formatTriple(rightedge), change)
####            printoutput(outstring, outfile)
###            xxxx = 1
###        elif (leftrow == rightrow) and (leftcol != rightcol):
####            outstring = '%s %s CHANGE COL  %3d' % (formatTriple(leftedge), \
####                                             formatTriple(rightedge), change)
####            printoutput(outstring, outfile)
###            if change > maxColDel: maxColDel = change
###        elif (leftrow != rightrow) and (leftcol == rightcol):
####            outstring = '%s %s CHANGE ROW  %3d' % (formatTriple(leftedge), \
####                                             formatTriple(rightedge), change)
####            printoutput(outstring, outfile)
###            if change > maxRowIns: maxRowIns = change
###        elif (leftrow == rightrow) and (leftcol == rightcol):
####            outstring = '%s %s CHANGE NO   %3d' % (formatTriple(leftedge), \
####                                             formatTriple(rightedge), change)
####            printoutput(outstring, outfile)
###            xxxx = 1
###        else:
###            outstring = '%s %s ERROR' % (leftedge, rightedge)
###            printoutput(outstring, outfile)
###            printoutput('', outfile)
###
###    return maxColDel, maxRowIns

#######################################################################
## find the min fraction in a block of the matrix
def findMinFrac(begin1, end1, sents1, begin2, end2, sents2, matrix, DUMMY):
    theMinDist = DUMMY
    theMinFrac = DUMMY
    theMinRow = DUMMY
    theMinCol = DUMMY

    newMinDistDel = DUMMY
    newMinFracDel = DUMMY
    newMinRowDel = DUMMY
    newMinColDel = DUMMY

    newMinDistIns = DUMMY
    newMinFracIns = DUMMY
    newMinRowIns = DUMMY
    newMinColIns = DUMMY

#    print('FINDMINFRAC (%d %d) (%d %d)' % (begin1,end1,begin2,end2))
    for i in range(begin1, end1+1):
        for j in range(begin2, end2+1):
#            if i == j: continue # why did i do this?
            thisDist = matrix[i][j][0] # matrix entries are [dist,del,ins]
            adjustedDistDel = matrix[i][j][0] - matrix[i][j][1]
            adjustedDistIns = matrix[i][j][0] - matrix[i][j][2]

            if sents1[i].isaligned():
                thisDist = 99999
            if sents2[j].isaligned():
                thisDist = 99999
            leftLen = sents1[i].getlength()
            rightLen = sents2[j].getlength()
            thisFrac = float(thisDist)/(float(leftLen) + float(rightLen))

            adjustedFracDel = float(adjustedDistDel)/(float(leftLen) + float(rightLen) - matrix[i][j][1])
            adjustedFracIns = float(adjustedDistIns)/(float(leftLen) + float(rightLen) - matrix[i][j][2])
            if adjustedFracDel < newMinFracDel:
                newMinDistDel = adjustedDistDel
                newMinFracDel = adjustedFracDel
                newMinRowDel = i
                newMinColDel = j
            if adjustedFracIns < newMinFracIns:
                newMinDistIns = adjustedDistIns
                newMinFracIns = adjustedFracIns
                newMinRowIns = i
                newMinColIns = j

#            if thisDist < theMinDist:
            if thisFrac < theMinFrac:

                if (1 == sents1[i].getlength()) and \
                       (1 == sents2[j].getlength()) and \
                           (2 == thisDist):
#                    outfile.write('BOGUS MATCH B (%d %s) (%d %s)\n' % \
#                          (i, sents1[i], j, sents2[j]))
                    continue
                if (1 == sents1[i].getlength()) and \
                       (2 == sents2[j].getlength()) and \
                           (3 == thisDist):
#                    outfile.write('BOGUS MATCH C (%d %s) (%d %s)\n' % \
#                          (i, sents1[i], j, sents2[j]))
                    continue
                if (2 == sents1[i].getlength()) and \
                       (1 == sents2[j].getlength()) and \
                           (3 == thisDist):
#                    outfile.write('BOGUS MATCH D (%d %s) (%d %s)\n' % \
#                          (i, sents1[i], j, sents2[j]))
                    continue

                theMinDist = thisDist
                theMinFrac = thisFrac
                theMinRow = i
                theMinCol = j

#    if newMinRowDel != theMinRow:
#        print('ZORKROWDEL %3d %3d' % (newMinRowDel, theMinRow))
#    if newMinRowIns != theMinRow:
#        print('ZORKROWINS %3d %3d' % (newMinRowIns, theMinRow))

#    if newMinColDel != theMinCol:
#        print('ZORKCOLDEL %3d %3d' % (newMinColDel, theMinCol))
#    if newMinColIns != theMinCol:
#        print('ZORKCOLINS %3d %3d' % (newMinColIns, theMinCol))

    minA = [theMinDist, theMinFrac, theMinRow, theMinCol]
    minB = [newMinDistDel, newMinFracDel, newMinRowDel, newMinColDel]
    minC = [newMinDistIns, newMinFracIns, newMinRowIns, newMinColIns]
    return [minA, minB, minC]

######################################################################
## format a line of info about aligned sentences
def formatAlignedSentenceInfo(label, name, s1, sub1, s2, sub2, theChar):
    outstring = ''
    stars = (s1.getalignmentlevel()) * '*'
    outstring = '%s %s DIST (LEFT RIGHT) %4d %c (%5s %5s) %-5s' % \
        (name, label, \
        s1.getdistance(), \
        theChar, \
        s1.formatsub(sub1), \
        s2.formatsub(sub2), \
        stars)
    outstring += '       %3d %3d %3d' % \
                   (s1.getlength(), s2.getlength(), \
                    s1.getlength()+s2.getlength())
    if s1.getdistance() > 0:
        outstring += ' %10.3f' % s1.geteditdistfracofworst()

        outstring += ' bagsizes %3d %3d %3d %5.2f %5.2f' % \
                     (s1.getlenbag(), \
                      s2.getlenbag(), \
                      s1.getleninter(), \
                      s1.getbagsizefrac(), \
                      s2.getbagsizefrac())

    return outstring

######################################################################
## format a line of info about deleted sentences
def formatDeletedSentenceInfo(label, name, s1, sub1):
    outstring = ''
    outstring = '%s %s                           %5s         %s' % \
        (name, label, s1.formatsub(sub1), 'DELETION')
    return outstring

######################################################################
## format a line of info about aligned sentences
def formatInsertedSentenceInfo(label, name, s2, sub2, theChar):
    outstring = ''
    outstring = '%s %s                        %c        %5s            %s %4d' % \
        (name, label, theChar, s2.formatsub(sub2), 'INSERTION', \
         s2.getpreviousdistance())
    return outstring

#######################################################################
### print the triples from the gap computation below
#def formatTriple(trip):
#    s = '[ %2d, %2d, %2d]' % (trip[0], trip[1], trip[2])
#    return s

######################################################################
## get the alignment statistics
def getalignmentstats(label, name, sents1, sents2, outfile):
    alignmentstats = ReturnedValues()

    for sent in sents1:
        alignmentstats.incrementstats(name, 'DRAFT', sent)
    
    for sent in sents2:
        alignmentstats.incrementstats(name, 'FINAL', sent)
    
    return alignmentstats

#######################################################################
### match the stanford tagged sentence with the corpus sentence
#def matchStanfordWithCorpus(corpussent, stanfordsent):
#    corpuslength = len(corpussent)
#    stanfordlength = len(stanfordsent)
#    lentotest = stanfordlength
#    if corpuslength < lentotest: lentotest = corpuslength
#
#    returnvalue = True
#    corpussub = 0
#    stanfordsub = 0
#    while (corpussub < lentotest) and (stanfordsub < lentotest):
#        if corpussent[corpussub] == '\x92':
#            corpussub += 1
#        if corpussent[corpussub] == '\x93':
#            corpussub += 1
#        if corpussent[corpussub] == '\x94':
#            corpussub += 1
#        if corpussent[corpussub] == "'":
#            corpussub += 1
#            print('NEXTENTRY', corpussent[corpussub])
#            if corpussent[corpussub] == "s":
#                corpussub += 1
#                print('NEXTENTRY2', corpussent[corpussub])
#
#        if stanfordsent[stanfordsub] == "'s":
#            stanfordsub += 1
#        if stanfordsent[stanfordsub] == "'":
#            stanfordsub += 1
#        if stanfordsent[stanfordsub] == "`":
#            stanfordsub += 1
#
#        print('COMPARE X%sX Y%sY' % (corpussent[corpussub], stanfordsent[stanfordsub]))
#        if corpussent[corpussub] != stanfordsent[stanfordsub]:
#            outstring = 'ERROR X%sX Y%sY' % (corpussent[corpussub], stanfordsent[stanfordsub])
#            printoutput(outstring, outfile)
#            returnvalue = False
#            break
#
#        corpussub += 1
#        stanfordsub += 1
#
#    return returnvalue

######################################################################
## print alignments, new version 6 april 2015
def printAlignmentsNew2(label, name, sents1, sents2, outfile):
#    alignmentStats = ReturnedValues()
    outstring = '%s %s NEW MATCH ALIGNMENTS BY SENT NUM\n' % (name, label)
    printoutput(outstring, outfile)

#    # first we deal with initial insertions in the final
#    if not sents2[0].isaligned():
#        sub2 = 0
#        while (sub2 < len(sents2)) and \
#              (not sents2[sub2].isaligned()):
##            print('INITIAL INSERTION %4d %s' % (sub2, sents2[sub2]))
#            outstring = formatInsertedSentenceInfo(label, name, \
#                                                   sents2[sub2], sub2, 'I')
#            printoutput(outstring, outfile)
##            alignmentStats.incrementAlignmentDictNew(name, 'FINAL', sents2[sub2])
#            sub2 += 1

    # now we run the loop on sents in the draft
    prevFinalSub = -1 
#    previousAlignedDistance = -1
    for sub1 in range(0, len(sents1)):
#        outstring = 'TESTCOMPARE %4d' % (sub1)
#        printoutput(outstring, outfile)

        # deletions
        if (not sents1[sub1].isaligned()):
#            outstring = 'DELETION %4d' % (sub1)
#            print(outstring)
#            printoutput(outstring, outfile)
            outstring = formatDeletedSentenceInfo(label, name, \
                                                  sents1[sub1], sub1)
            printoutput(outstring, outfile)
#            alignmentStats.incrementAlignmentDictNew(name, 'DRAFT', sents1[sub1])

        else: # draft is aligned to something
            finalSub = sents1[sub1].getalignmentsub()
            if finalSub != prevFinalSub+1:
#                outstring = 'FINAL INSERTION %4d %4d %4d' % (sub1, prevFinalSub, finalSub)
#                printoutput(outstring, outfile)
                for sub2 in range(prevFinalSub+1, finalSub):
#                    outstring = 'LOOP FINAL INSERTION %4d %4d %4d %4d' % (sub1, prevFinalSub, finalSub, sub2)
#                    printoutput(outstring, outfile)
                    if sents2[sub2].isaligned():
                        loopDraftSub = sents2[sub2].getalignmentsub()
                        # if it was aligned, then save the distance
#                        previousAlignedDistance = sents1[loopDraftSub].getdistance()
                        outstring = formatAlignedSentenceInfo(label, name, \
                                          sents1[loopDraftSub], loopDraftSub, \
                                          sents2[sub2], sub2, 'M')
                        outstring += ' MISALIGN?'
                        printoutput(outstring, outfile)
#                        alignmentStats.incrementAlignmentDictNew(name, \
#                                                                 'DRAFT', \
#                                                                 sents1[sub1])
                    else:
#                        sents2[sub2].setpreviousdistance(previousAlignedDistance)
                        outstring = formatInsertedSentenceInfo(label, name, \
                                          sents2[sub2], sub2, 'M')
                        outstring += ' MISALIGN?'
                        printoutput(outstring, outfile)

#                        alignmentStats.incrementAlignmentDictNew(name, \
#                                                                 'FINAL', \
#                                                                 sents2[sub2])


            # if it was aligned, then save the distance
#            previousAlignedDistance = sents1[sub1].getdistance()

            outstring = formatAlignedSentenceInfo(label, name, \
                                                   sents1[sub1], sub1, \
                                                   sents2[finalSub], finalSub, ' ')
            printoutput(outstring, outfile)
#            alignmentStats.incrementAlignmentDictNew(name, 'DRAFT', sents1[sub1])
            prevFinalSub = finalSub


    # we set the value of the previous edit distance
    # first the initial insertions
    previousAlignedDistance = -1
    previousAlignmentSub = -1
    for sentSub in range(0, len(sents2)):
        sent = sents2[sentSub]
        sent.setpreviousdistance(previousAlignedDistance)
        sents2[sentSub] = sent
        if sent.isaligned():
            previousAlignedDistance = sent.getdistance()
            previousAlignmentSub = sent.getalignmentsub()
#        else:
#            previousAlignedDistance = -1


    alignmentStats = getalignmentstats(label, name, sents1, sents2, outfile)
    return alignmentStats

#######################################################################
### print the list of sentences, each of which is a list
#def printSentences(label, sentences, outfile):
#    for sent in sentences:
#        s = label + ' ' + ' '.join(sent)
#        outstring = '%s' % (s)
#        printoutput(outstring, outfile)

######################################################################
## determine whether or not we skip this paragraph
## note that the third parameter is the number of the last para
## indexed from zero and is not the number of paragraphs
def skipthispara(sentence, paratype, numlastpara):
    TAG = 'MAIN: SKIPTHIS:'
    paraNumber = sentence.getparasub()
    if ('ALL' == paratype):
#        outstring = '%s do ALL    paratype %s and paraNumber %d, PROCESS' % \
#                     (TAG, paratype, paraNumber)
#        printoutput(outstring, outfile)
        return False

    if ('FIRST' == paratype) and (0 == paraNumber):
#        outstring = '%s do FIRST  paratype %s and paraNumber %d, PROCESS' % \
#                     (TAG, paratype, paraNumber)
#        printoutput(outstring, outfile)
        return False
    elif ('LAST' == paratype) and (numlastpara == paraNumber):
#        outstring = '%s do LAST   paratype %s and paraNumber %d of %d, PROCESS' % \
#                     (TAG, paratype, paraNumber, numlastpara)
#        printoutput(outstring, outfile)
        return False
    elif ('MIDDLE' == paratype) \
                    and (paraNumber > 0) \
                    and (paraNumber < numlastpara):
#        outstring = '%s do MIDDLE paratype %s and paraNumber %d of %d, PROCESS' % \
#                     (TAG, paratype, paraNumber, numlastpara)
#        printoutput(outstring, outfile)
        return False
    else:
#        outstring = '%s           paratype %s and paraNumber %d, SKIP' % \
#                     (TAG, paratype, paraNumber)
#        printoutput(outstring, outfile)
        return True
        
    return False

#######################################################################
### skip the word entirely under some conditions
#def skipthisword(word):
#    skipIt = False
#    if word == '.': skipIt = True
#    elif word == ',': skipIt = True
#    elif word == '.,': skipIt = True
#    elif word == ',"': skipIt = True
#    elif word == ';': skipIt = True
#    elif word == '?': skipIt = True
#    elif word == '!': skipIt = True
#    elif word == '[': skipIt = True
#    elif word == ']': skipIt = True
#    elif word == '-': skipIt = True
#    elif word == '--': skipIt = True
#    elif word == '---': skipIt = True
#    elif word == '"--': skipIt = True
#    elif word == '!--': skipIt = True
#    elif word == '(!': skipIt = True
#    elif word == '(': skipIt = True
#    elif word == ')': skipIt = True
#    elif word == '(?': skipIt = True
#    elif word == ').': skipIt = True
#    elif word == '"': skipIt = True
#    elif word == "'": skipIt = True
##    elif word == 'I': skipIt = True
#    elif word == 'I.': skipIt = True
#    elif word == 'II': skipIt = True
#    elif word == 'II.': skipIt = True
#    elif word == 'III': skipIt = True
#    elif word == 'III.': skipIt = True
#    elif word == 'IV': skipIt = True
#    elif word == 'IV.': skipIt = True
#    elif word == 'V': skipIt = True
#    elif word == 'V.': skipIt = True
#    elif word == 'VI': skipIt = True
#    elif word == 'VI.': skipIt = True
#    elif word == 'VII': skipIt = True
#    elif word == 'VII.': skipIt = True
#    elif word == 'VIII': skipIt = True
#    elif word == 'VIII.': skipIt = True
#    elif word == 'IX': skipIt = True
#    elif word == 'IX.': skipIt = True
#    elif word == 'X': skipIt = True
#    elif word == 'X.': skipIt = True
#    elif word == 'XI': skipIt = True
#    elif word == 'XI.': skipIt = True
#    elif word == 'XII': skipIt = True
#    elif word == 'XII.': skipIt = True
#    elif word == 'XIII': skipIt = True
#    elif word == 'XIII.': skipIt = True
#
#    return skipIt

#################################################################################
#### use the stanford tagger to tag sentences with POS
#def stanfordtag(pathtodata, name):
#    filenameinput = pathtodata + '/' + name
#    command='stanford-postagger.sh models/english-bidirectional-distsim.tagger'
#    filenameoutput = 'xxxxtaggeroutput.txt'
#    callargument = '%s %s >%s' % (command, filenameinput, filenameoutput)
#    SP.call(callargument, shell=True)
#
#    wcoutput = SP.check_output('wc -l ' + filenameoutput, shell=True)
#    linecount = int(wcoutput.split()[0])
##    print('LINECOUNT ', linecount)
#
#    taggerfile = open(filenameoutput)
#    taggedlines = []
#    linesread = 0
#    for line in taggerfile:
#        taggedlines.append(line)
#        linesread += 1
##        print('LINESREAD %3d of %3d' % (linesread, linecount))
#        if linesread >= linecount:
#            break
#    taggerfile.close()
##    print('LENGTH %3d' % (len(taggedlines)))
#
##    for num, line in enumerate(taggedlines):
##        outstring = '%s %s TAGGED: %3d: %s' % (TAG, idnumber, num, line)
##        printoutput(outstring, outfile)
#
#    taggedlineswithouttags = []
#    for line in taggedlines:
#        oneline = []
#        for token in line.split():
##            print('TOKEN %s' % (token))
#            tokensplit = token.split('_')
#            oneline.append(tokensplit[0])
#        taggedlineswithouttags.append(oneline)
#
##    for num, line in enumerate(taggedlines):
##        outstring = '\n%s %s TAGGEDWITH:    %3d: %s' % (TAG,idnumber,num,line)
##        printoutput(outstring, outfile)
##        outstring = '%s %s TAGGEDWITHOUT: %3d: %s' % (TAG, idnumber, num, \
##                     taggedlineswithouttags[num])
##        printoutput(outstring, outfile)
#
#    return taggedlines, taggedlineswithouttags

################################################################################
### use the stanford tagger to tag a paragraph with POS
def stanfordtagpara(paranum, para):
    paratext = ''
    for sentence in para:
        sentencejoined = ' '.join(sentence)
        paratext += ' ' + sentencejoined

    filenameinput = 'xxxxoutputpara%03d' % (paranum)
    outfile = open(filenameinput, 'w')
    outfile.write('%s' %(paratext))
    outfile.close()

    command='stanford-postagger.sh models/english-bidirectional-distsim.tagger'
    filenameoutput = 'xxxxtaggeroutput.txt'
    callargument = '%s %s >%s' % (command, filenameinput, filenameoutput)
    SP.call(callargument, shell=True)

    wcoutput = SP.check_output('wc -l ' + filenameoutput, shell=True)
    linecount = int(wcoutput.split()[0])
#    print('LINECOUNT ', linecount)

    taggerfile = open(filenameoutput)
    taggedlines = []
    linesread = 0
    for line in taggerfile:
        taggedlines.append(line)
        linesread += 1
#        print('LINESREAD %3d of %3d' % (linesread, linecount))
        if linesread >= linecount:
            break
    taggerfile.close()
#    print('LENGTH %3d' % (len(taggedlines)))

#    for num, line in enumerate(taggedlines):
#        outstring = '%s %s TAGGED: %3d: %s' % (TAG, idnumber, num, line)
#        printoutput(outstring, outfile)

    taggedlineswithouttags = []
    taggedlineswithtags = []
    for line in taggedlines:
        onelinewithtags = []
        onelinewithouttags = []
        for token in line.split():
#            print('TOKEN %s' % (token))
            tokensplit = token.split('_')
            onelinewithtags.append(token)
            onelinewithouttags.append(tokensplit[0])
#        print('WITHTAGS    %s' % (onelinewithtags))
#        print('WITHOUTTAGS %s' % (onelinewithouttags))
        taggedlineswithtags.append(onelinewithtags)
        taggedlineswithouttags.append(onelinewithouttags)

#    for num, line in enumerate(taggedlines):
#        outstring = '\n%s %s TAGGEDWITH:    %3d: %s' % (TAG,idnumber,num,line)
#        printoutput(outstring, outfile)
#        outstring = '%s %s TAGGEDWITHOUT: %3d: %s' % (TAG, idnumber, num, \
#                     taggedlineswithouttags[num])
#        printoutput(outstring, outfile)

    return taggedlineswithtags, taggedlineswithouttags

#1234567890123456789012345678901234567890123456789012345678901234567890123456789
################################################################################
## MAIN BODY OF CODE
## main body of code

## Command line arguments for this block
checkArgs(5, "usage: a.out pathtodata outfilename paragraphs alignmentandbags")

################################################################################
## parse the command line and open files
outfilename = sys.argv[2]
if 'stdout' == outfilename:
    outfile = sys.stdout
else:
    outfile = open(outfilename, 'w')

## measure process and wall clock times
mytimer = MyTimer()
outstring, cputimelist = mytimer.timecall('MAIN: AT BEGINNING')
printoutput(outstring, outfile)

################################################################################
## determine which paragraphs to analyze
outstring = "MAIN: DETERMINE WHICH PARAS TO ANALYZE"
printoutput(outstring, outfile)
paratype = sys.argv[3]
if 'FIRST' == paratype:
    outstring = 'MAIN: We do the FIRST paragraph'
elif 'MIDDLE' == paratype:
    outstring = 'MAIN: We do the MIDDLE paragraphs'
elif 'LAST' == paratype:
    outstring = 'MAIN: We do the LAST paragraph'
elif 'ALL' == paratype:
    outstring = 'MAIN: We do ALL paragraphs'
else:
    outstring = "ERROR: paragraphs must be "
    outstring += "'FIRST', 'LAST', 'MIDDLE', or 'ALL', "
    outstring += "not '%s'" % (paratype)
    printoutput(outstring, outfile)
    sys.exit()
printoutput(outstring, outfile)

################################################################################
## determine when to quit with the alignment
outstring = "MAIN: DETERMINE WHEN TO QUIT WITH THE ALIGNMENT"
printoutput(outstring, outfile)
alignmentandbags = sys.argv[4]
if ('ALIGNBAGLIMIT' != alignmentandbags) and \
   ('ALIGNBAGNO' != alignmentandbags):
    outstring = "ERROR: alignmentandbags neither ALIGNBAGLIMIT NOR ALIGNBAGNO\n"
    printoutput(outstring, outfile)
    sys.exit()

if 'ALIGNBAGLIMIT' == alignmentandbags:
    ALIGNMAX = 0.50
    BAGMIN = 0.50
elif 'ALIGNBAGNO' == alignmentandbags:
    ALIGNMAX = 1.00
    BAGMIN = 0.00
outstring = "MAIN: ALIGNMAX = %f and BAGMIN = %f\n" % (ALIGNMAX, BAGMIN)
printoutput(outstring, outfile)

################################################################################
## determine the path to the data
outstring = "MAIN: DETERMINE THE PATH TO THE DATA"
printoutput(outstring, outfile)
pathtodata = sys.argv[1]
outstring = "MAIN: PATH='%s' OUTFILE='%s'" % (pathtodata, outfilename)
printoutput(outstring, outfile)

filenames = listdir(pathtodata)
outstring = 'MAIN: DIRECTORY: %s' % (pathtodata)
printoutput(outstring, outfile)

################################################################################
## get the stopwords for later
outstring = "MAIN: GET THE STOPWORDS"
printoutput(outstring, outfile)
stopfile = open('xstoplistNLTK.txt')
stops = stopfile.read().split()
stopwords = set(stops)
stopfile.close()

################################################################################
## call the timer after the initial parsing of command line and the
## reading of the stopword file
outstring, cputimelist = mytimer.timecall('MAIN: AFTER ARGPARSE')
printoutput(outstring, outfile)

################################################################################
## read the files and put them into the dictionary
## note that there's a tedious glitch here in that we have draft and
## final to match up, so we need to make sure we have both and not
## just one of the two
##
## what we get from this is a dictionary 'versions' whose 'name'-th
## subscript is the a list of two items, the nltk object for the
## draft paper and the nltk object for the final paper
##
outstring = "MAIN: GET THE FILES THEMSELVES"
printoutput(outstring, outfile)
versions = {}
for longname in filenames:
    if longname.startswith('.'): continue
    parsedname = longname.split('_')
    namesemester = parsedname[0]
    namecourse = parsedname[1]
    namesection = parsedname[2]
    shortname = parsedname[3]
    print('V%sV W%sW X%sX Y%sY Z%sZ' % (parsedname, namesemester, namecourse, namesection, shortname))

    if shortname.endswith('1.txt'):
        nametype = 1
    elif shortname.endswith('2.txt'):
        nametype = 2
    elif shortname.endswith('3.txt'):
        nametype = 3
    elif shortname.endswith('4.txt'):
        nametype = 4
    else:
        print('ERROR TYPE %s\n' % (name))
        sys.exit()
    idnumber = '%11s_%1s' % (longname[0:11], nametype)

    TAG = 'MAIN: CREATECLEAN:'
    outstring = '%s %s READ FILE: %s' % (TAG, idnumber, pathtodata+'/'+longname)
    printoutput(outstring, outfile)

    doc = nltk.corpus.PlaintextCorpusReader(pathtodata, longname, \
                                            encoding = 'ISO-8859-2')
    
    outstring = '%s %s %s CORPUS PARAS: %3d' % (TAG, idnumber, longname, \
                                                len(doc.paras()))
    printoutput(outstring, outfile)
    outstring = '%s %s %s CORPUS SENTS: %3d' % (TAG, idnumber, longname, \
                                                len(doc.sents()))
    printoutput(outstring, outfile)

    sentencelist = []

    # insert a bogus first sentence so that there will always
    # be an aligned sentence at the beginning of the document
    overallnumsent = 0
    numpara = 0
    if 'draft' in shortname:
        firstsentencedraft = Sentence(longname, 'DRAFT', numpara, \
                             overallnumsent, \
                             ['inserted', 'first', 'sentence'], \
                             ['inserted_VBN', 'first_JJ', 'sentence_NN'], \
                             stopwords)
        sentencelist.append(firstsentencedraft)
    else:
        firstsentencefinal = Sentence(longname, 'FINAL', numpara, \
                             overallnumsent, \
                             ['inserted', 'first', 'sentence'], \
                             ['inserted_VBN', 'first_JJ', 'sentence_NN'], \
                             stopwords)
        sentencelist.append(firstsentencefinal)

    # for each paragraph (as per PlainTextCorpusReader) run the
    # stanford POS tagger on the paragraph and then add the instances
    # of those sentences on to the running list of 'sentence' objects
    for numpara, para in enumerate(doc.paras()):
        outstring = '%s %s %s CORPUS PARAS SENTS: %3d %3d' % \
                    (TAG, idnumber, longname, numpara, len(para))
        printoutput(outstring, outfile)

        # get the lists of lines with and without tags
        outstring = '%s %s %s TAG PARA NUM: %3d %3d' % \
                    (TAG, idnumber, longname, numpara, len(para))
        printoutput(outstring, outfile)
        taggedlines, taggedlineswithouttags = stanfordtagpara(numpara, para)

        # check that the lists are consistent with each other
        taggedcount = len(taggedlines)
        if taggedcount != len(taggedlineswithouttags):
            outstring = '%s %s %s ERROR TAGGED COUNTS: %3d %3d' % \
                        (TAG, idnumber, longname, taggedcount, \
                         len(taggedlineswithouttags))
            printoutput(outstring, outfile)
            sys.exit()
        else:
            outstring = '\n%s %s %s TAGGED COUNTS AGREE: %3d %3d' % \
                        (TAG, idnumber, longname, taggedcount, \
                         len(taggedlineswithouttags))
            printoutput(outstring, outfile)

        # now append the sentences to the running list
        for numsent, sent in enumerate(taggedlines):
            overallnumsent += 1
            if 'draft' in shortname:
                thissentence = Sentence(longname, 'DRAFT', numpara, \
                                        overallnumsent, \
                                        taggedlineswithouttags[numsent], \
                                        sent, \
                                        stopwords)
            else:
                thissentence = Sentence(longname, 'FINAL', numpara, \
                                        overallnumsent, \
                                        taggedlineswithouttags[numsent], \
                                        sent, \
                                        stopwords)
            sentencelist.append(thissentence)

    # insert a bogus last sentence so that there will always
    # be an aligned sentence at the very end of the document
    numpara = len(doc.paras())
    overallnumsent += 1
    if 'draft' in shortname:
        lastsentencedraft = Sentence(longname, 'DRAFT', numpara-1, \
                            overallnumsent, \
                            ['inserted', 'last', 'sentence'], \
                            ['inserted_VBN', 'last_JJ', 'sentence_NN'], \
                            stopwords)
        sentencelist.append(lastsentencedraft)
    else:
        lastsentencefinal = Sentence(longname, 'FINAL', numpara-1, \
                            overallnumsent, \
                            ['inserted', 'last', 'sentence'], \
                            ['inserted_VBN', 'last_JJ', 'sentence_NN'], \
                            stopwords)
        sentencelist.append(lastsentencefinal)

##    # dump the sentence list
##    for num, item in enumerate(sentencelist):
##        outstring = '\n%s %s LIST: %3d %3d: %s' % (TAG, idnumber, item.getparasub(), num, item)
##        printoutput(outstring, outfile)
##
##        outstring = '%s %s LIST: %3d %3d: %s' % (TAG, idnumber, item.getparasub(), num, item.getsent())
##        printoutput(outstring, outfile)
##
##        outstring = '%s %s LIST: %3d %3d: %s' % (TAG, idnumber, item.getparasub(), num, item.getTaggedSent())
##        printoutput(outstring, outfile)

#zork

### the following function also adds a dummy first and last sentence
### forcing initial changes and final changes to be inside an alignment 
#    createCharacterCleanedFile(TAG, pathtodata, name)

#    version = nltk.corpus.PlaintextCorpusReader('.', 'zzzztemp'+name, \
#                                                 encoding = 'utf-8')
#    for sent in version.sents():
#        outstring = '%s zork %s %s' % (idnumber, name, sent)
#        printoutput(outstring, outfile)
#    sys.exit(0)

    # the 'versions' dictionary has a list pair as its target
    # the pair is [draftlistofsentences, finalistofsentences]
    theversion = []
    TAG = 'MAIN: READCLEAN:  '
    if 'draft' in shortname:
        if idnumber in versions.keys():
            outstring = '%s %s draft, name, number %s' % (TAG, idnumber, longname)
            printoutput(outstring, outfile)
            theversion = versions[idnumber]
            theversion[DRAFT] = sentencelist
            versions[idnumber] = theversion

#           remember the sentence count is bogus high by two for dummy sents
            outstring = '%s %s DRAFTWORDSSENTSA: %s %d\n' % \
                        (TAG, idnumber, longname, len(sentencelist)-2)
            printoutput(outstring, outfile)
        else:
            outstring = '%s %s draft, not name, number %s' % (TAG,idnumber,longname)
            printoutput(outstring, outfile)
            theversion = [sentencelist, 'dummy']
            versions[idnumber] = theversion

#           remember the sentence count is bogus high by two for dummy sents
            outstring = '%s %s DRAFTWORDSSENTSB: %s %d\n' % \
                        (TAG, idnumber, longname, len(sentencelist)-2)
            printoutput(outstring, outfile)
        
    else:
        if idnumber in versions.keys():
            outstring = '%s %s final, name, number %s' % (TAG, idnumber, longname)
            printoutput(outstring, outfile)
            theversion = versions[idnumber]
            theversion[FINAL] = sentencelist
            versions[idnumber] = theversion

#           remember the sentence count is bogus high by two for dummy sents
            outstring = '%s %s FINALWORDSSENTSA: %s %d\n' % \
                        (TAG, idnumber, longname, len(sentencelist)-2)
            printoutput(outstring, outfile)
        else:
            outstring = '%s %s final, not name, number %s' % (TAG,idnumber,longname)
            printoutput(outstring, outfile)
            theversion = ['dummy', sentencelist]
            versions[idnumber] = theversion

#           remember the sentence count is bogus high by two for dummy sents
            outstring = '%s %s FINALWORDSSENTSB: %s %d\n' % \
                        (TAG, idnumber, longname, len(sentencelist)-2)
            printoutput(outstring, outfile)

## measure process and wall clock times
outstring, cputimelist = mytimer.timecall('AFTER READ')
printoutput(outstring, outfile)

################################################################################
## now we run the main loop in the code

profiler = LinguisticProfiler(stopwords) # we need globals for this class

for name, version in sorted(versions.items()):
    TAG = 'MAIN: NAME:'
    outstring = '%s PROCESSING %s' % (TAG, longname)
    printoutput(outstring, outfile)

    version1 = version[DRAFT]
    version2 = version[FINAL]

    lastsentence1 = version1[len(version1)-1]
    lastsentence2 = version2[len(version2)-1]
    numlastpara1 = lastsentence1.getparasub()
    numlastpara2 = lastsentence2.getparasub()

# this may be low by one because it's subscript indexed from 0
    outstring = '%s %s ZORKPARACOUNTS     %5d %5d' % \
                    (TAG, longname, numlastpara1, numlastpara2)
    printoutput(outstring, outfile)

#   remember the sentence count is bogus high by two for dummy sents
    outstring = '%s %s ZORKSENTENCECOUNTS %5d %5d' % \
                (TAG, longname, len(version1)-2, len(version2)-2)
    printoutput(outstring, outfile)

    ############################################################################
    ## append the sentences onto the two lists of sentences
    sentSub = -1 
    sents1 = []
    for sent in version1:
        if skipthispara(sent, paratype, numlastpara1): continue
        sents1.append(sent)

    sentSub = -1 
    sents2 = []
    for sent in version2:
        if skipthispara(sent, paratype, numlastpara2): continue
        sents2.append(sent)

    ############################################################################
    # now is as good a time to do linguistic profiling as any
    # we have spent some time in converting the corpus reader 'version'
    # into two lists of instances of 'sentence', so we will use those
    # lists and not the original text
    outstring = '%s %s WE DO THE PROFILE\n' % (TAG, longname)
    printoutput(outstring, outfile)

    profiler.doprofile(longname, 'DRAFT', sents1, outfile)
    profiler.doprofile(longname, 'FINAL', sents2, outfile)

    outstring = '%s %s WE HAVE DONE THE PROFILE\n' % (TAG, longname)
    printoutput(outstring, outfile)

    ##################################################################
    # control the size of the computation
    # this is the max number of sentences in the doc to try to align
    sentenceComparisonCount1 = 200
    sentenceComparisonCount2 = 200
    outerLimit = min(sentenceComparisonCount1, len(sents1))
    innerLimit = min(sentenceComparisonCount2, len(sents2))
    outstring = '%s %s WE COMPARE THE FIRST (%d, %d) SENTS (INCLUDING BOGUS)\n' % \
                (TAG, longname, outerLimit, innerLimit)
    printoutput(outstring, outfile)

    ## measure process and wall clock times
    outstring, cputimelist = mytimer.timecall('AFTER LENGTHS')
    printoutput(outstring, outfile)

    ##################################################################
    ## we need a big matrix of pairwise distances of sentences
    distanceMatrix = []
    for sub1 in range(0, outerLimit):
        rowDist = []
        for sub2 in range(0, innerLimit):
            rowDist.append([0, 0, 0])
        distanceMatrix.append(rowDist)

#    displaySubmatrix(name, 0, outerLimit-1, 0, innerLimit-1, distanceMatrix)

    ## measure process and wall clock times
    outstring, cputimelist = mytimer.timecall('AFTER INIT')
    printoutput(outstring, outfile)

    ##################################################################
    ## start the process of getting the list to align
    ## and we definitely want to align the bogus first and last sents
    matchList = []
    midList = []
    for sub1 in range(0, outerLimit):
        if 0 == sub1 % 5:
            outstring = '%s OUTER LOOP PROGRESS ... %5s' % \
                         (longname, sents1[sub1].formatsub(sub1))
            printoutput(outstring, outfile)
        if sents1[sub1].getalignmentsub() != ALIGNMENTDUMMYSUB:
#            outstring = 'ALREADY USED1 %d %d' % (sub1, sents2[sub1].getAlignment())
#            printoutput(outstring, outfile)
            continue
        for sub2 in range(0, innerLimit):
            if sents2[sub2].getalignmentsub() != ALIGNMENTDUMMYSUB:
#                outstring = 'ALREADY USED2 %d %d' % (sub2, sents2[sub2].getAlignment())
#                printoutput(outstring, outfile)
                continue
#            outstring = 'TEST %d %d' % (sub1, sub2)
#            printoutput(outstring, outfile)

            editInstance = EditDistance(sents1[sub1], sents2[sub2])
            distanceList = editInstance.computedistance(outfile)
            distance = distanceList[0]
            maxColDel = distanceList[1]
            maxRowIns = distanceList[2]

#            editInstance.display2(outfile)

            distanceMatrix[sub1][sub2] = distanceList
#            distanceMatrix[sub1][sub2] = distance
#            outstring = 'TEST %3d %3d %3d' % (sub1, sub2, distance)
#            printoutput(outstring, outfile)
            if 0 == distance: 
                appendedLine = [sub1, sub2, distance, 0]
#                outstring = 'APPENDED LINEA %s' % (appendedLine)
#                printoutput(outstring, outfile)
                matchList.append(appendedLine)

                thisLevel = 0
#                print('SETALIGNA %d %d %d' % (sub1, sub2, thisLevel))
                sents1[sub1].setalignment(thisLevel, sents2[sub2], distance)
                sents2[sub2].setalignment(thisLevel, sents1[sub1], distance)
                break
            elif distance <= 2: 
                # if distance is 2 but each sentence is one word, continue
                if (1 == sents1[sub1].getlength()) and \
                   (1 == sents2[sub2].getlength()):
                    continue

                appendedLine = [sub1, sub2, distance, 0]
#                outstring = 'APPENDED LINEB %s' % (appendedLine)
#                printoutput(outstring, outfile)
                matchList.append(appendedLine)

                thisLevel = 0
#                print('SETALIGNB %d %d %d' % (sub1, sub2, thisLevel))
                sents1[sub1].setalignment(thisLevel, sents2[sub2], distance)
                sents2[sub2].setalignment(thisLevel, sents1[sub1], distance)
                break

    ##################################################################
    ## done with the zero alignment
    ##
    ## measure process and wall clock times
    outstring, cputimelist = mytimer.timecall('AFTER ZEROETH')
    printoutput(outstring, outfile)

#    for sent in sents1:
#        print('%s' % (sent)) 
#        otherSentSub = sent.getalignmentsub()
#        if ALIGNMENTDUMMYSUB != otherSentSub:
#            print('%s' % (sents2[otherSentSub])) 
#            print('')

    label = 'ZEROETH ALIGNMENT'

#    printAlignmentList(label, name, matchList, outfile, \
#                       sents1, sents2, ALIGNMAX, BAGMIN)
#    returnedValues = printAlignmentList(label, name, matchList, outfile, \
#                                        sents1, sents2, ALIGNMAX, BAGMIN)
#    printAlignmentsNew(label, name, sents1, sents2, outfile)
    alignmentStats = printAlignmentsNew2(label, longname, sents1, sents2, outfile)

#    for key, oldvalue in sorted(returnedValues.getalignmentdict().items()):
#        outstring = 'OLDDICT1 %19s %5d' % (key, oldvalue)
#        printoutput(outstring, outfile)
#

    ##################################################################
    ## score the success in terms of number of sentences aligned now
    draftSentenceCount = 0
    finalSentenceCount = 0
    for key, value in sorted(alignmentStats.getalignmentdict().items()):
        outstring = 'NEWDICT1 %19s %5d' % (key, value)
        if int(key.split()[1]) < 799:
            draftSentenceCount += value
            finalSentenceCount += value
        if int(key.split()[1]) == 799:
            draftSentenceCount += value
        if int(key.split()[1]) == 899:
            finalSentenceCount += value
        printoutput(outstring, outfile)
    outstring = 'NEWDICT1 DRAFTCOUNT %5d' % (draftSentenceCount)
    printoutput(outstring, outfile)
    outstring = 'NEWDICT1 FINALCOUNT %5d' % (finalSentenceCount)
    printoutput(outstring, outfile)
#zork 2015 09 07

    #displaySubmatrix(0, outerLimit-1, 0, innerLimit-1, distanceMatrix)
#zork
#    misalignments = returnedValues.getMisalignments()
#    outstring = '%s ALIGNMENT COUNT LEVEL %4d %4d %4d    %4d %4d' % \
#                 (name, 0, len(matchList), len(matchList), \
#                  len(sents1)-len(matchList)+misalignments, \
#                  len(sents2)-len(matchList)+misalignments)
#    printoutput(outstring, outfile)

    ##################################################################
    ## now we do the main alignment loop
    labels = ['ZEROETH ALIGNMENT', 'FIRST   ', 'SECOND  ', 'THIRD   ', 'FOURTH  ', 'FIFTH   ', 'SIXTH   ', 'SEVENTH ', 'EIGHTH  ', 'NINTH   ', 'TENTH   ']
    for level in range(1, 11):
        label = labels[level]
        midList = []
        if level >= 0:
            midList = displayAligned(label, longname, matchList, sents1, sents2, \
                                     level, outfile, distanceMatrix, \
                                     ALIGNMAX, BAGMIN, True)
        else:
            midList = displayAligned(label, longname, matchList, sents1, sents2, \
                                     level, outfile, distanceMatrix, \
                                     ALIGNMAX, BAGMIN)
        matchList = matchList + midList
#        outstring = '%s ALIGNMENT COUNT LEVEL %4d  %4d %4d    %4d %4d' % (name, level, len(midList), len(matchList), len(sents1)-len(matchList), len(sents2)-len(matchList))
#        misalignments = returnedValues.getMisalignments()
#        outstring = '%s ALIGNMENT COUNT LEVEL %4d %4d %4d    %4d %4d' % \
#                     (name, 0, len(matchList), len(matchList), \
#                      len(sents1)-len(matchList)+misalignments, \
#                      len(sents2)-len(matchList)+misalignments)
#        printoutput(outstring, outfile)

        matchList = sorted(matchList)
#        printAlignmentList('AFTER '+label, name, matchList, outfile, \
#                            sents1, sents2, ALIGNMAX, BAGMIN)
#        returnedValues = printAlignmentList('AFTER '+label, name, matchList, outfile, \
#                                             sents1, sents2, ALIGNMAX, BAGMIN)
        alignmentStats = printAlignmentsNew2('AFTER '+label, longname, \
                                             sents1, sents2, outfile)

#        for key, oldvalue in sorted(returnedValues.getalignmentdict().items()):
#            outstring = 'OLDDICT2 %19s %5d' % (key, oldvalue)
#            printoutput(outstring, outfile)
#
        ##################################################################
        ## score the success in terms of number of sentences aligned now
        draftSentenceCount = 0
        finalSentenceCount = 0
        for key, value in sorted(alignmentStats.getalignmentdict().items()):
            outstring = 'NEWDICT2 %19s %5d' % (key, value)
            if int(key.split()[1]) < 799:
                draftSentenceCount += value
                finalSentenceCount += value
            if int(key.split()[1]) == 799:
                draftSentenceCount += value
            if int(key.split()[1]) == 899:
                finalSentenceCount += value
            printoutput(outstring, outfile)
        outstring = 'NEWDICT2 DRAFTCOUNT %5d' % (draftSentenceCount)
        printoutput(outstring, outfile)
        outstring = 'NEWDICT2 FINALCOUNT %5d' % (finalSentenceCount)
        printoutput(outstring, outfile)


        breakNow = False
        if 0 == len(midList):
            outstring = '%s ZORK_ALIGNMENT_COUNT_UNCHANGED_IN_LEVEL %d' % (longname, level)
            outstring += '  %4d %4d    %4d %4d' % (len(midList), len(matchList), len(sents1)-len(matchList), len(sents2)-len(matchList))
            printoutput(outstring, outfile)
            breakNow = True

        ## measure process and wall clock times
        outstring, cputimelist = mytimer.timecall('AFTER '+label)
        printoutput(outstring, outfile)

        if breakNow: break # put this here to allow for the timing just above

    ##################################################################
    ## alignment is done, now we output the results
    outstring = ''
    printoutput(outstring, outfile)

    outstring = '%s ZORKEDITDISTSLEGEND ' % (longname)
    outstring += 'Frequency counts of edit dist fracs and #s of sentences '
    printoutput(outstring, outfile)
    outstring = '%s ZORKEDITDISTSLEGEND ' % (longname)
    outstring += 'with those dists(799=del, 899=ins)'
    printoutput(outstring, outfile)

    alignmentDict = alignmentStats.getalignmentdict()
    for key, value in sorted(alignmentDict.items()):
        outstring = '%s ZORKEDITDISTS %s %4d' % (longname, str(key), value)
        printoutput(outstring, outfile)

    outstring = ''
    printoutput(outstring, outfile)

    outstring = '%s ZORKDELETIONSLEGEND ' % (longname)
    outstring += 'Number of deletions by para #'
    printoutput(outstring, outfile)
    outstring = '%s ZORKDELETIONSLEGEND ' % (longname)
    outstring += '(para_#, #_deletions)'
    printoutput(outstring, outfile)

    deletionsByPara = alignmentStats.getdeletionsbypara()
    for key, value in sorted(deletionsByPara.items()):
        outstring = '%s ZORKDELETIONS %s %4d' % (longname, str(key), value)
        printoutput(outstring, outfile)

    outstring = ''
    printoutput(outstring, outfile)

    outstring = '%s ZORKINSERTIONSLEGEND ' % (longname)
    outstring += 'Number of insertions by para #'
    printoutput(outstring, outfile)
    outstring = '%s ZORKINSERTIONSLEGEND ' % (longname)
    outstring += '(para_#, #_insertions)'
    printoutput(outstring, outfile)

    insertionsByPara = alignmentStats.getinsertionsbypara()
    for key, value in sorted(insertionsByPara.items()):
        outstring = '%s ZORKINSERTIONS %s %4d' % (longname, str(key), value)
        printoutput(outstring, outfile)

    outstring = ''
    printoutput(outstring, outfile)

#    # we used to need this, but we don't any more
#    outstring = '%s ZORKINSERTBYDISTLEGEND ' % (name)
#    outstring += 'Number of insertions by dist frac of previous sentence'
#    printoutput(outstring, outfile)
#    outstring = '%s ZORKINSERTBYDISTLEGEND ' % (name)
#    outstring += 'We count a block of inserted sentences as one instance'
#    printoutput(outstring, outfile)
#
#    insertionsByDist = returnedValues.getInsertionsByDist()
#    for key, value in sorted(insertionsByDist.items()):
#        outstring = '%s ZORKINSERTBYDIST %s %4d' % (name, str(key), value)
#        printoutput(outstring, outfile)
#
#    outstring = ''
#    printoutput(outstring, outfile)

    # similarities between edit dist frac and bagsize overlap
    outstring = '%s ZORKSIMILARITYLEGEND ' % (longname)
    outstring += 'bag_value_draft = bag_intersection/bag_draft'
    printoutput(outstring, outfile)
    outstring = '%s ZORKSIMILARITYLEGEND ' % (longname)
    outstring += 'bag_value_final = bag_intersection/bag_final'
    printoutput(outstring, outfile)
    outstring = '%s ZORKSIMILARITYLEGEND ' % (longname)
    outstring += '(dist/worst_case_edit)  (bag_value_draft)  (bag_value_final)'
    printoutput(outstring, outfile)

    for sent in sents1:
        if sent.isaligned():
            if sent.getdistance() > 0:
                thisBagSizeFrac = sent.getbagsizefrac()
                thatBagSizeFrac = sents2[sent.getalignmentsub()].getbagsizefrac()

                outstring = '%s ZORKSIMILARITY %5.2f %5.2f %5.2f' % \
                             (name, sent.geteditdistfracofworst(), \
                                    thisBagSizeFrac, \
                                    thatBagSizeFrac)
                printoutput(outstring, outfile)
    outstring = ''
    printoutput(outstring, outfile)

    # print in sorted order of edit distance
    listByDist = []
    listByBagFracDraft = []
    for sent in sents1:
        if sent.isaligned():
            if sent.getdistance() > 0:
                listByDist.append([sent.geteditdistfracofworst(), sent])
                listByBagFracDraft.append([sent.getbagsizefrac(), sent])
    for item in sorted(listByDist):
        sent = item[1]
        outstring ='%s ZORKEDITDISTFRACTION %4d<-->%4d %5.2f %4d %5.2f %5.2f'%\
                 (name, sent.getsentsub(), sent.getalignmentsub(), \
                        sent.geteditdistfracofworst(), \
                        sent.getdistance(), \
                        sent.getbagsizefrac(), \
                        sents2[sent.getalignmentsub()].getbagsizefrac())

        # we also used to print out the actual sentences here

        printoutput(outstring, outfile)
    listByDist = []

    ## measure process and wall clock times
#    timeBegin()
    outstring, cputimelist = mytimer.timecall('THREE ' + name)
    printoutput(outstring, outfile)


    # print in reverse sorted order of word bag intersection
#    for item in listByBagFracDraft:
#        print('TEST1595 %s' % (item))
    for item in sorted(listByBagFracDraft, reverse=True):
#    for item in listByBagFracDraft.sort(reverse=True):
        sent = item[1]
        outstring ='%s ZORKSENTENCESBAGS %4d<-->%4d %5.2f %4d %5.2f %5.2f'%\
                 (name, sent.getsentsub(), sent.getalignmentsub(), \
                        sent.geteditdistfracofworst(), \
                        sent.getdistance(), \
                        sent.getbagsizefrac(), \
                        sents2[sent.getalignmentsub()].getbagsizefrac())
        printoutput(outstring, outfile)
    listByBagFracDraft = []

    ##################################################################
    ## now we output the sentences in draft and final along with all
    ## the other information we have in the sentence class
    for sent in sents1:
        outstring = 'ZZNEW     %s' % (sent)
        printoutput(outstring, outfile)

    for sent in sents2:
        outstring = 'ZZNEW     %s' % (sent)
        printoutput(outstring, outfile)

    ##################################################################
    ## and we output the insertions and the deletions
    for sent in sents1:
        if sent.isdeletion():
            outstring = 'ZZNEW DEL %s' % (sent)
            printoutput(outstring, outfile)
            outstring = 'ZZNEW DEL %s' % (sent.stringthesent())
            printoutput(outstring, outfile)

    for sent in sents2:
        if sent.isinsertion():
            outstring = 'ZZNEW INS %s' % (sent)
            printoutput(outstring, outfile)
            outstring = 'ZZNEW INS %s' % (sent.stringthesent())
            printoutput(outstring, outfile)

######################################################################
## summary information for timing purposes

profiler.printglobalresults('GLOBAL', 'XXXXX', outfile)

label = 'AT END:'
outstring, cputimelist = mytimer.timecall(label)
printoutput(outstring, outfile)

outstring = '\nNUMBER OF PAPERS %4d' % (len(versions))
printoutput(outstring, outfile)

timePerPaper = cputimelist[1] / len(versions)
outstring = '%s TIME [CURRENT, TOTAL] = [%10.3f, %10.3f], PER PAPER = %10.3f' % \
             (label, cputimelist[0], cputimelist[1], timePerPaper)
printoutput(outstring, outfile)

outstring = "%s DRAFT AND FINAL TOGETHER COUNT AS 'ONE' PAPER" % (label)
printoutput(outstring, outfile)
