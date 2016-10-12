'''
Created on Oct 6, 2016

@author: boningliang
'''
import datetime
import xml.dom.minidom
from xml.dom.minidom import parse
import time, datetime
import math
import Angle

class Fix(object):


    def __init__(self, logFile = 'log.txt'):
        functionName = "Fix.__init__: "
        

        
        if not isinstance(logFile, basestring):
            raise ValueError(functionName)
        
        self.logFile = logFile
        self.sightingFile = ''
        self.approximateLatitude = "0d0.0"
        self.approximateLongitude = "0d0.0"
        try:
            self.logFile = open(logFile,'r')
        except IOError:
            self.logFile = open(logFile, 'w')
        else:
            self.logFile = open(logFile,'a')
            
        self.startOfLog()

    def setSightingFile(self, sightingFile):
        self.sightingFile = sightingFile
        self.startOfSightingFile()
        try:
            open(sightingFile, 'r')
            return False
        except:
            open(sightingFile, 'w')
            return True
            
    def getSightings(self):
        sightingHeader = "LOG: "
        dateTimeOfWrite = ""
        entryString = ""
        domTree = xml.dom.minidom.parse(self.sightingFile)
        sightingTree = domTree.documentElement
        sightings = sightingTree.getElementsByTagName("sighting")
        
        for sighting in sightings:
            entryString = sightingHeader
            dateTimeOfWrite = self.getDateTime()
            entryString += dateTimeOfWrite + " "
            
            if not len(sighting.getElementsByTagName("horizon")[0].childNodes) == 0:
                theHorizon = sighting.getElementsByTagName("horizon")[0].childNodes[0].data
            else:
                theHorizon = "Natural" 
    
            if not len(sighting.getElementsByTagName("height")[0].childNodes) == 0:
                theHeight = float(sighting.getElementsByTagName("height")[0].childNodes[0].data)
            else:
                theHeight = 0
            
            if theHeight == "":
                theHeight = 0
            
            if not len(sighting.getElementsByTagName("pressure")[0].childNodes) == 0:
                thePressure = float(sighting.getElementsByTagName("pressure")[0].childNodes[0].data)
            else:
                thePressure = 1010              
            
            if not len(sighting.getElementsByTagName("temperature")[0].childNodes) == 0:
                theTemperature = float(sighting.getElementsByTagName("temperature")[0].childNodes[0].data)
            else:
                theTemperature = 72
            
            theAltitude = sighting.getElementsByTagName("observation")[0].childNodes[0].data
            
            altitudeAngle = Angle.Angle()
            observedAltitude = altitudeAngle.setDegreesAndMinutes(theAltitude)

            theHeight = float(theHeight)
            
            adjustedAltitude = self.calculateAdjustedAltitude(theHorizon, theHeight, thePressure, theTemperature, observedAltitude)
            
            adjustedAltitudeAngle = Angle.Angle()
            adjustedAltitudeAngle.setDegrees(adjustedAltitude)
            adjustedAltitudeAngleStr = adjustedAltitudeAngle.getString()
            
            entryString += sighting.getElementsByTagName("body")[0].childNodes[0].data + "\t"
            entryString += sighting.getElementsByTagName("date")[0].childNodes[0].data + "\t"
            entryString += sighting.getElementsByTagName("time")[0].childNodes[0].data + "\t"
            
            entryString += str(adjustedAltitudeAngleStr)
            
#             entryString += self.adjustedAltitude(sighting.getElementsByTagName("time")[0].childNodes[0].data)
            self.logFile.write(entryString+"\n")
            self.logFile.flush()

            entryString = ""
            
        self.EndOfLog()
        
        return (self.approximateLatitude, self.approximateLongitude)

    def getAttributes(self):
        pass

# private
    def FahrenheitToCelsius(self, fahrenheit):
        celsius = (float(fahrenheit) - 32 ) / 1.8
        return celsius

# private
    def adjustedAltitude(self, altitude = 0):
        return "0d0.0"
#private
    def calculateAdjustedAltitude(self, theHorizon, theHeight, thePressure, theTemperature, observedAltitude):
        if theHorizon == "Natural":
            dip = (-0.97 * math.sqrt(theHeight)) / 60.0
        else:
            dip = 0.0
            
        refraction = (0.00452 * float(thePressure)) / (273 + self.FahrenheitToCelsius(theTemperature)) / math.atan(observedAltitude)
        
        adjustedAltitude = observedAltitude + dip + refraction
        return adjustedAltitude

#     private    
    def startOfLog(self):
        self.logFile.write(self.entryHeader() + "Start of log\n")
        self.logFile.flush()

    def startOfSightingFile(self):
        self.logFile.write(self.entryHeader() + "Start of sighting file: " +self.sightingFile+"\n")
        self.logFile.flush()

#     private    
    def EndOfLog(self):
        self.logFile.write(self.entryHeader() + "End of sighting file: " +self.sightingFile+"\n")
        self.logFile.flush()
    
#     private    
    def entryHeader(self):
        entryHeader = "LOG: " + self.getDateTime() + " "
        return entryHeader
    
#     private
    def getDateTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         return datetime.datetime.now()
    
    
    
    
    
    
    
    
    
    
    
    
    