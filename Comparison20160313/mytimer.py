import time
#from dabfunctions import printoutput

######################################################################
## TIMER CLASS
class MyTimer():
    def __init__(self):
        self._timecpuprev = time.clock()
        self._timewallclockbegin = time.time();
        self._timewallclockprev = self._timewallclockbegin

######################################################################
##
    def timecall(self, label):
        self._timecpunext = time.clock()
        self._timewallclocknext = time.time()
        self._timecpu = self._timecpunext - self._timecpuprev
        self._timewallclockCurr = self._timewallclocknext - self._timewallclockprev
        self._timewallclockTotal = self._timewallclocknext - self._timewallclockbegin

        if self._timewallclockCurr > 0.0:
            self._percent = 100.00 * (self._timecpu / self._timewallclockCurr)
            if self._percent > 100.00:
                self._percent = 100.00
        else:
            self._percent = 100.00

        outstring = 'TIME*******************************************************************\n'
        outstring += 'TIME %-20s %7.3f  %10.3f user   %10.3f wall\n' % \
                     (label, self._percent, self._timecpu, self._timewallclockCurr)
        outstring += 'TIME %-20s          %10.3f user_t %10.3f wall_t\n' % \
                     (label, self._timecpunext, self._timewallclockTotal)
        outstring += 'TIME*******************************************************************' # don't need the newline character

        self._timecpuprev = self._timecpunext
        self._timewallclockprev = self._timewallclocknext

        # return the output string
        # and [cpu time of this interval,  cpu time total]
        return outstring, [self._timecpu, self._timecpunext]
