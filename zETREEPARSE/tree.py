################################################################################
## Program to read the 'parse' output of the Stanford Core NLP package
## and create a DOM-like tree structure so the complexity of sentences can
## be analyzed.
##
## Each line in the file is a separate parsed sentence. 
## For each line,
##     XML-ize the line by turning open parens into open XML tags
##         and closing parens into closing tags
##     write that to a file (because I can't get the XML parsing to
##         work except by reading from a file
##     parse that file as an 'ElementTree' parse
##
##     then call a recursive function to descend through the parse tree
##

import sys
import xml.etree.ElementTree as ET

################################################################################
## descend recursively from a given node
## 
## print the level and the tag and the text at this level
## then get the children of this node and descend in the same function
## 
def descend(level, node):
    children = list(node)
    childrencount = len(children)
    for childsub, child in enumerate(children):
        tag = child.tag.strip()
        text = child.text.strip()
        atts = child.attrib
        if int(atts['level']) != level:
            print('ERROR ATTS, LEVEL: %d %d' % (atts['level'], level))
            sys.exit()
        print('%s %3d CHILD %3d of %3d  %-12s %s' % \
                   (level*'   ', level, childsub, childrencount, tag, text))
        level += 1
        descend(level, child)
        level -= 1

################################################################################
## function to print a list with a label and a 'level' variable
def printlist(label, level, thelist):
    print(label, len(thelist))
    for item in thelist:
        print('%3d: %s' % (level, item))

################################################################################
## function to display the xml
##
## the big deal here is just to keep track of the nesting level
## so as to indent an appropriate number of spaces
def stringifyxml(thexml):
    outstring = ''
    nesting = 0
    nestingspaces = '    '
    for item in thexml:
        label = item[0]
        content = item[1] 
        if 'OPEN' == label:
            ## the 'nesting-1' is because the 'ROOT' is level 0 but
            ## that outer XML tag is ignored by the 'ElementTree' code
            outstring += '%s<%s level="%d">\n' % \
                          (nesting*nestingspaces, content, nesting-1)
            nesting += 1
        elif 'CLOSE' == label:
            nesting -= 1
            outstring += '%s</%s>\n' % (nesting*nestingspaces, content)
        else:
            # nesting += 1
            outstring += '%s%s\n' % (nesting*nestingspaces, content)
            # nesting -= 1

    return outstring

################################################################################
## function to xml-ize a line of tokens
##
## We want to turn open parens into open XML tags and close parens into
## close tags.`
## We do this with a bit of a hack.
## Convert open parens into paren plus blank space, and close parens into
## close preceded by blank space.
## This allows the 'split' function to create separate tokens. 
## 
## We then run through the tokens.
##     if an open paren we create an open tag and push the tag on a stack
##     if just data, we use the data
##     if a close paren, we pop the stack to know what kind of close tag
##         to create 
def xmlize(line):
    line = line.replace('(', '( ')
    line = line.replace(')', ' )')
    line = line.replace('<parse>(', '<parse> ( ')
    print('NEW', line)

    linesplit = line.split()
    print(linesplit)
    rewrite = [] 

    tokensub = 0
    mostrecenttags = []
    while tokensub < len(linesplit):
        token = linesplit[tokensub]
        if '<parse>' == token:
            tokensub += 1
            continue
        if '</parse>' == token:
            tokensub += 1
            continue
#        print(tokensub, token)

        if '(' == token:
            tokensub += 1
            nexttoken = linesplit[tokensub]
            if '.' == nexttoken:
                nexttoken = 'PERIOD'
            mostrecenttags.append(nexttoken)
            nextnexttoken = linesplit[tokensub+1]
            rewrite.append(['OPEN', nexttoken])
            if '(' != nextnexttoken:
                rewrite.append(['DATA', nextnexttoken])
                tokensub += 1
#        print(rewrite)
        if ')' == token:
            rewrite.append(['CLOSE', mostrecenttags.pop()])
        tokensub += 1

    return rewrite

################################################################################
## main Main MAIN
thefile = open('xx.txt', encoding='utf-8')
lines = []
for line in thefile:
    xml = xmlize(line)
    print(xml)
    xmlstring = stringifyxml(xml)
    print(xmlstring)

    outfile = open('xmloutfile.txt', 'w')
    outfile.write(xmlstring)
    outfile.close()

    tree = ET.parse('xmloutfile.txt')

    level = 0
    root = tree.getroot()
    descend(level, root)

