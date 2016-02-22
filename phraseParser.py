# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 13:55:45 2016

@author: Federica Clementi
"""

import re
from bs4 import BeautifulSoup
from glob import glob


####################################################################
## A bit of a hack to get all xml elements into a list

def xmlList(soup):
    # use prettify to get each tag on separate line, then convert to ascii
    uni = soup.prettify()
    xmlString = uni.encode('ascii', 'ignore')
    
    #split on line break to create a list
    xmlList = xmlString.split('\n')
    
    #now strip the white spaces from each item in the list
    newXmlList = []
    
    for item in xmlList:
        item = item.strip()
        newXmlList.append(item)
        
    return newXmlList[2:-2]    #slice gets rid of the html and body tags added by prettify

######################################################################
# Returns a 2D list with each item in the form: for instance, ['open', 'nn']

def xmlPairs(xmlList):
    newList = []
    regex = re.compile(r'<\w+') #for capturing tag name
    
    for item in xmlList:
        if item.startswith('</'):
            tag = item.rstrip('>')
            tag = tag[2:]
            newList.append(['close', tag])
        elif item.startswith('<'):
            tagName = regex.findall(item)
            
            if tagName:
                tag = tagName[0].lstrip('<')    #findall() returns a list
                newList.append(['open', tag])
        else:
            newList.append(['word', item])
            
    return newList
    
#######################################################################
## This function collects all phrases of a specified type.
## Input includes a list of tag types and tag names/values: e.g.,
## ['close', 'np'] or ['word', 'apple']. It returns a list of
## all occurences of the specified phrase type.
    
def getPhrases(tagList, tag):
    
    # initialize two variables to count opening and closing phrase tags;
    # use a boolean to track when the loop is in a target phrase type
    openTag = 0
    closeTag = 0
    activeTag = False
    currentPhrase = []
    allPhrases = []
    
    for pair in tagList:
        if pair[0] == 'open' and pair[1] == tag:
            openTag += 1
            activeTag = True
        
        # keep adding pairs while in a target phrase
        if activeTag:
            currentPhrase.append(pair)
            
        if pair[0] == 'close' and pair[1] == tag:
            closeTag += 1
            # if openTag == closeTag, we've reached the end of a phrase
            if openTag == closeTag:
                allPhrases.append(currentPhrase)
                #re-initialize all variables for next phrase search
                openTag = 0
                closeTag = 0
                activeTag = False
                currentPhrase = []
                
    return allPhrases

########################################################################

def verifyXML(tagList):
    
    stack = []
    
    for pair in tagList:
        
        # push
        if pair[0] == 'open' or pair[0] == 'word':
            stack.append(pair)
        
        # pop and compare
        else:
            popped = stack.pop()
            
            if popped[0] == 'word':
                popped = stack.pop()
                
                if popped[1] == pair [1]:
                    continue
                else:
                    return 'Ill-formed xml'
           
    return 'Well-formed xml'
        
#######################################################################
# Returns the average phrase length
        
def avgPhraseLen(allPhrases):
    wordCount = 0
    for phrase in allPhrases:
        for elem in phrase:
            if elem[0] == 'word':
                wordCount += 1
                
    return float(wordCount)/float(len(allPhrases))
    
########################################################################
def countSent(tagList):
    count = 0
    for pair in tagList:
        if pair[0] == 'open' and pair[1] == 'root':
            count += 1
            
    return count
    
########################################################################
class XMLTree:
    
    def __init__(self, soup):
        self.soup = soup
        self.tags = xmlList(self.soup)
        self.pairs = xmlPairs(self.tags)
        
        
########################################################################
#
# MAIN PROGRAM
#
#######################################################################
    
#xmldoc = open('oneSent.xml')
#xmldoc = open('oneSent2.xml')
#xmldoc = open('academicOneSent.xml')
#xmldoc = open('data/academic/xmlAcademicParses.xml')
#xmldoc = open('data/student/001Final1.xml')
#xmldoc = open('out.txt')
#xmldoc = open('data/fiction/witw.xml')
xmldoc = open('data/atlantic/atlantic.xml')
    
soup = BeautifulSoup(xmldoc)
# create a list of tag types and tag names/values
xList = xmlList(soup)
xPairs = xmlPairs(xList)

allPhrases = getPhrases(xPairs, 'vp')


print
print len(allPhrases)
print 'Average Phrase Length: ', avgPhraseLen(allPhrases)

"""
# CODE FOR STUDENT PAPERS

filePaths = glob('data/student/*.xml')
filePairs = []

for i in range(0, len(filePaths) - 1, 2):
    filePairs.append([filePaths[i], filePaths[i+1]])

  
draftSentCount = 0
finalSentCount = 0
count = 0
allDraftAvg = 0
allFinalAvg = 0
draftPhraseLenAvg = 0
finalPhraseLenAvg = 0

for pair in filePairs:
    
    count += 1
    
    xmldraft = open(pair[0])
    xmlfinal = open(pair[1])
    
    soupdraft = BeautifulSoup(xmldraft)
    soupfinal = BeautifulSoup(xmlfinal)
    
    #create a list of all xml elements:
    draftList = xmlList(soupdraft)
    finalList = xmlList(soupfinal)
    
    # create a 2D list of tag type and tag name/value: e.g.,
    # ['open', 'nn'] or ['close', 'nn']:
    
    draftPairs = xmlPairs(draftList)
    finalPairs = xmlPairs(finalList)
        
    draftSentCount += countSent(draftPairs)
    finalSentCount += countSent(finalPairs)
    
    # create a list of all instances of target phrase type
    draftPhrases = getPhrases(draftPairs, 'np')
    finalPhrases = getPhrases(finalPairs, 'np')
    
    draftAvg = avgPhraseLen(draftPhrases)
    finalAvg = avgPhraseLen(finalPhrases)
    
    allDraftAvg += draftAvg
    allFinalAvg += finalAvg
    
    #draftPhraseLenAvg += draftAvg
    #finalPhraseLenAvg += finalAvg
    
    allDraftAvg += len(draftPhrases)
    allFinalAvg += len(finalPhrases)
    
    
    print '%-15s %-15f %-15f' % (pair[0][13:16], draftAvg, finalAvg)
    
print 'Average NP length: ', float(allDraftAvg)/float(count), float(allFinalAvg)/float(count)

"""