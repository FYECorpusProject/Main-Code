from collections import defaultdict

class Histogram(object):

    ##################################################################
    ## fill out a dictionary with zero entries in between max and min key
    @staticmethod
    def fillOutZeros(theDict, outFile):
        # now fill out the zero entries
        keys = theDict.keys()
        keys = sorted(keys)
#        print('%s' % (keys))
        keymin = keys[0]
        if 799 in keys:
            keys.remove(799)
        if 888 in keys:
            keys.remove(888)
        if 899 in keys:
            keys.remove(899)
        if 999 in keys:
            keys.remove(999)
        if len(keys) > 0:
            keymax = keys[-1] # ignore 799, 899, 999
        else:
            keymax = -1 # ignore 799, 899, 999
#        print('min and max %d %d' % (keymin, keymax))
#        outFile.write('min and max %d %d\n' % (keymin, keymax))
        for sub in range(keymin, keymax+1):
            if sub not in theDict.keys():
                theDict[sub] = 0

        return theDict

    ##################################################################
    ## histogram the data
    ##
    ## note that this fills out the dictionary with zeros as needed for
    ## a real histogram
    ##
    ## parameters:
    ##     theDataDict - the dictionary to histo
    ##     maxAgg - the smallest value to aggregate by
    ##     maxAgg - the largest value to aggregate by
    ##     outFile - the output file to which to write
    @staticmethod
    def histoTheData(label, theDataDict, minAgg, maxAgg, outFile):
        theDataDictWithZeros = Histogram.fillOutZeros(theDataDict, outFile)

        s = ''
        shortVersion = []
        for agg in range(minAgg, maxAgg+1):
            localDict = defaultdict(int)
            totalCount = 0
            maxBucket = 0
            for key,value in sorted(theDataDictWithZeros.items()):
                bucket = (key // agg) * agg
                localDict[bucket] += value 
                if localDict[bucket] > maxBucket: maxBucket = localDict[bucket]
                totalCount += value

            divideDown = 1
            if maxBucket > 50:
                divideDown = (maxBucket // 50) + 1

            s += '\n' + label + 'AGGREGATE BY %3d: EACH LINE IS A SPREAD OF %d\n' \
                   % (agg, agg)
            s += 'TOTAL COUNT OF DATA POINTS IS %5d\n' % (totalCount)
            s += 'EACH STAR REPRESENTS UP TO %3d DATA POINT(S)\n' % (divideDown)
            for key,value in sorted(localDict.items()):
                pct = float(100 * value) / float(totalCount)
                if 799 == key+agg-1:
                    sLine = 'DEL       %5.1f %5d: ' % (pct, value)
                elif 899 == key+agg-1:
#                    sLine = '    INS   %5.1f %5d: ' % (pct, value)
                    sLine = 'BEGINNING %5.1f %5d: ' % (pct, value)
                elif 999 == key+agg-1:
                    sLine = 'UNALIGN   %5.1f %5d: ' % (pct, value)
                else:
                    sLine = '%3d-%3d   %5.1f %5d: ' % (key, key+agg-1, pct, value)
                s += sLine
                for i in range(0, value, divideDown):
                    s += '*' 
                s += '\n' 

#                if key <= 10:
#                    shortVersion.append(sLine)

#                if (sLine.startswith('  0-')) or (sLine.startswith('    INS')):
#                    shortVersion.append(sLine)

                if sLine.startswith('  0-') or sLine.startswith('    INS') \
                                            or sLine.startswith('DEL'):
                    shortVersion.append(sLine)

        return s, shortVersion
