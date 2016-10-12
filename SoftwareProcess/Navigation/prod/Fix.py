'''
Created on Oct 6, 2016

@author: boningliang
'''

class Fix(object):


    def __init__(self, logFile = 'log.txt'):
        self.logFile = logFile
        try:
            self.logFile = open(logFile,'r')
        except IOError:
            self.logFile = open(logFile, 'w')
        else:
            self.logFile = open(logFile,'a')
