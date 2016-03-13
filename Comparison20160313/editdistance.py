import sys
from dabfunctions import printoutput

######################################################################
## EDIT DISTANCE
##
## We pad the lists to make the matrix doublesize and square.
## This allows us to go down the off diagonal from row 1 all the
##    way down left, and then we pick off the distance
##    we need from the lengths of the original lists.
class EditDistance():

    ##################################################################
    ## initialization
    def __init__(self, sent1, sent2):
        self._origsent1 = sent1.getsent() # just pick off the actual sentences
        self._origsent2 = sent2.getsent() # just pick off the actual sentences

        self._padded1 = ['NULL'] + self._origsent1
        self._padded2 = ['NULL'] + self._origsent2

        self._squaresize = 2 * max(len(self._padded1), len(self._padded2))
        for sub in range(len(self._padded1), self._squaresize):
            self._padded1.append('x')
        for sub in range(len(self._padded2), self._squaresize):
            self._padded2.append('y')

        self.initmatrix() # initializes self._matrix

    ##################################################################
    ## backtrack to get edit path
    def backtrack(self):
        backtracklist = []
        row = len(self._origsent2)
        col = len(self._origsent1)
        dist = self._matrix[row][col]

#        print('ROW COL DIST %3d %3d %3d' % (row, col, dist))
        backtracklist.append([row, col, dist])
        while (row > 0) or (col > 0):
            if row > 0:
                valueup = self._matrix[row-1][col]
                if col > 0: # row and col both > 0
                    valueleft = self._matrix[row][col-1]
                    valuediag = self._matrix[row-1][col-1]
                else: # row > 0, col = 0
                    valuediag = 999999
                    valueleft = 999999

            else: # row = 0
                valuediag = 999999
                valueup = 999999
                if col > 0: # row = 0, col > 0
                    valueleft = self._matrix[row][col-1]
                else: # row = 0, col = 0
                    valueleft = 999999

            if (valuediag <= valueleft) and (valuediag <= valueup):
                row -= 1
                col -= 1
                dist = valuediag
            elif (valueup <= valuediag) and (valueup <= valueleft):
                row -= 1
                dist = valueup
            elif (valueleft <= valuediag) and (valueleft <= valueup):
                col -= 1
                dist = valueleft
            else:
                print('ERROR VALUES %3d %3d %3d' % (valuediag, valueleft, valueup))

#            print('ROW COL DIST %3d %3d %3d' % (row, col, dist))
            backtracklist.append([row, col, dist])
        backtracklist.reverse()
        return backtracklist

    ##################################################################
    ## computedistances
    def computedistance(self, outfile):
        rowcolsum = 2
        while rowcolsum < self._squaresize:
            row = rowcolsum - 1
            col = rowcolsum - row
            while row > 0:
                if self._padded1[col] == self._padded2[row]:
                    self._matrix[row][col] = self._matrix[row-1][col-1]
#                    print 'MATCH OK  ', row, col, self._padded1[col], self._padded2[row]
                else:
                    value1 = self._matrix[row][col-1] + 1
                    value2 = self._matrix[row-1][col] + 1
                    value3 = self._matrix[row-1][col-1] + 2
                    self._matrix[row][col] = min(value1, value2, value3)
#                    print 'MATCH FAIL  ', row, col, self._padded1[col], self._padded2[row]
                row -= 1
                col += 1
#            self.display()
            rowcolsum += 1
        origlen1 = len(self._origsent1)
        origlen2 = len(self._origsent2)
#        self.display()

        # note that we use original lengths, because we padded with 'NULL' 
#        print('RETURN ROW,COL,DIST (%d %d) %d' % (origLen2, origLen1, \
#                                                  self._matrix[origLen2][origLen1]))
        maxcoldel, maxrowins = self.computegapdistances(outfile)

        return [self._matrix[origlen2][origlen1], maxcoldel, maxrowins]
#        return self._matrix[origlen2][origlen1]

    ##################################################################
    ## compute the max insertion and deletion gaps
    def computegapdistances(self, outfile):
#        outString = '\nEDIT: DRAFT %s' % (self._padded1)
#        printoutput(outString, outfile)
#        outString = 'EDIT: FINAL %s' % (self._padded2)
#        printoutput(outString, outfile)
 
        backtracklist = self.backtrack()
#        outString = 'EDIT: BACKTRACK %s' % (backtracklist)
#        printoutput(outString, outfile)

        # find the row insert/delete instances
        maxrowcount = 0
        maxcolcount = 0
        # prepend a dummy to start off the computation
        alignedpairs = [[[0, 0, 0], [0, 0, 0]]]
        for listsub in range(0, len(backtracklist)-1):
            thiselt = backtracklist[listsub]
            thisrow = thiselt[0]
            thiscol = thiselt[1]
            thisval = thiselt[2]
 
            nextelt = backtracklist[listsub+1]
            nextrow = nextelt[0]
            nextcol = nextelt[1]
            nextval = nextelt[2]
 
            if (thisrow != nextrow) and \
               (thiscol != nextcol) and \
               (thisval == nextval):
                alignedpairs.append([thiselt, nextelt])
 
        alignedpairs.append([nextelt, [nextrow+1, nextcol+1, nextval]])
#        outString = 'EDIT: ALIGNED   %s' % (alignedpairs)
#        printoutput(outString, outfile)
 
#        for item in alignedpairs:
#            outString = '%s %s' % (formatTriple(item[0]), formatTriple(item[1]))
#            printoutput(outString, outfile)
#        outString = ''
#        printoutput(outString, outfile)

        maxColDel = 0
        maxRowIns = 0
        for listsub in range(0, len(alignedpairs)-1):
            thiselt = alignedpairs[listsub]
            leftedge = thiselt[1]
            leftrow = leftedge[0]
            leftcol = leftedge[1]
            leftval = leftedge[2]

            nextelt = alignedpairs[listsub+1]
            rightedge = nextelt[0]
            rightrow = rightedge[0]
            rightcol = rightedge[1]
            rightval = rightedge[2]

            change = rightval - leftval

            # column changes are deletions from draft
            # row changes are insertions into final
            if (leftrow != rightrow) and (leftcol != rightcol):
#                outString = '%s %s CHANGE BOTH %3d' % (self.formatTriple(leftedge), \
#                                         self.formatTriple(rightedge), change)
#                printoutput(outString, outfile)
                xxxx = 23
            elif (leftrow == rightrow) and (leftcol != rightcol):
#                outString = '%s %s CHANGE DEL  %3d' % (self.formatTriple(leftedge), \
#                                         self.formatTriple(rightedge), change)
#                printoutput(outString, outfile)
                if change > maxColDel: maxColDel = change
            elif (leftrow != rightrow) and (leftcol == rightcol):
#                outString = '%s %s CHANGE INS  %3d' % (self.formatTriple(leftedge), \
#                                         self.formatTriple(rightedge), change)
#                printoutput(outString, outfile)
                if change > maxRowIns: maxRowIns = change
            elif (leftrow == rightrow) and (leftcol == rightcol):
#                outString = '%s %s CHANGE NO   %3d' % (self.formatTriple(leftedge), \
#                                         self.formatTriple(rightedge), change)
#                printoutput(outString, outfile)
                xxxx = 23
            else:
#                outString = '%s %s ERROR' % (leftedge, rightedge)
#                printoutput(outString, outfile)
#                printoutput('', outfile)
                xxxx = 23

#        outString = 'EDIT: MAX DEL INS %3d%3d' % (maxColDel, maxRowIns)
#        printoutput(outString, outfile)

        return maxColDel, maxRowIns

    ######################################################################
    ## print the triples from the gap computation below
    def formatTriple(self,trip):
        s = '[ %2d, %2d, %2d]' % (trip[0], trip[1], trip[2])
        return s

#    ##################################################################
#    ## display the edit distance matrix
#    def display(self):
#        print('')
#        printstring = '%4s: ' % (' ')
#        for col in range(0, self._squaresize):
#            printstring += ' %4s' % (self._padded1[col][0:4])
#        print('%s' % (printstring))
#    
#        for row in range(0, self._squaresize):
#            printstring = '%4s: ' % (self._padded2[row][0:4])
#            for col in range(0, self._squaresize):
#                printstring += ' %4s' % (self._matrix[row][col])
#            print('%s' % (printstring))

#    ##################################################################
#    ## display the edit distance matrix
#    def display2(self, outfile):
##        print('')
#        printoutput('', outfile)
#        printstring = '    %4s: ' % (' ')
#        for col in range(0, len(self._origsent1)+1):
#            printstring += ' %4d' % (col)
##        print('%s' % (printstring))
#        printoutput(printstring, outfile)
#        printstring = '    %4s: ' % (' ')
#        for col in range(0, len(self._origsent1)+1):
#            printstring += ' %4s' % (self._padded1[col][0:4])
##        print('%s' % (printstring))
#        printoutput(printstring, outfile)
#    
#        for row in range(0, len(self._origsent2)+1):
#            printstring = '%3d %4s: ' % (row, self._padded2[row][0:4])
#            for col in range(0, len(self._origsent1)+1):
#                printstring += ' %4s' % (self._matrix[row][col])
##            print('%s' % (printstring))
#            printoutput(printstring, outfile)
#
    ##################################################################
    ## initialize a matrix for the distance computation
    def initmatrix(self):
        self._matrix = []
        _row = []
        _row.append(0)
        for _colsub in range(1, self._squaresize):
            _row.append(_colsub)
        self._matrix.append(_row)

        for _rowsub in range(1, self._squaresize):
            _row = []
            _row.append(_rowsub)
            for _colsub in range(1, self._squaresize):
                _row.append(0)
            self._matrix.append(_row)

## end of EditDistance class
######################################################################
