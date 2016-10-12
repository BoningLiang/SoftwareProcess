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

    def setSightingFile(self, sightingFile):
        self.sightingFile = sightingFile
        try:
            open(sightingFile, 'r').close()
            return True
        except IOError:
            pass
        else:
            return False
            
    def getSightings(self):
        sightingHeader = "LOG: "
        dateTimeOfWrite = ""
        entryString = ""
        domTree = xml.dom.minidom.parse("sightingFile.xml")
        sightingTree = domTree.documentElement
        sightings = sightingTree.getElementsByTagName("sighting")
        
        self.startOfLog()
        
        for sighting in sightings:
            entryString = sightingHeader
            dateTimeOfWrite = self.getDateTime()
            entryString += dateTimeOfWrite + " "
            theHorizon = sighting.getElementsByTagName("horizon")[0].childNodes[0].data
            theHeight = sighting.getElementsByTagName("height")[0].childNodes[0].data
            thePressure = sighting.getElementsByTagName("pressure")[0].childNodes[0].data
            theTemperature = sighting.getElementsByTagName("temperature")[0].childNodes[0].data
            theAltitude = sighting.getElementsByTagName("observation")[0].childNodes[0].data
            
            altitudeAngle = Angle.Angle()
            observedAltitude = altitudeAngle.setDegreesAndMinutes(theAltitude)
            
            theHeight = float(theHeight)
            
            if theHorizon == "Natural":
                dip = (-0.97 * math.sqrt(theHeight)) / 60
            else:
                dip = 0.0
            
            refraction = (0.00452 * float(thePressure)) / (273 + self.FahrenheitToCelsius(theTemperature)) / math.atan(observedAltitude)
            
            adjustedAltitude = observedAltitude + dip + refraction
            
            adjustedAltitudeAngle = Angle.Angle()
            adjustedAltitudeAngle.setDegrees(adjustedAltitude)
            adjustedAltitudeAngleStr = adjustedAltitudeAngle.getString()
            
            entryString += sighting.getElementsByTagName("body")[0].childNodes[0].data + "\t"
            entryString += sighting.getElementsByTagName("date")[0].childNodes[0].data + "\t"
            entryString += sighting.getElementsByTagName("time")[0].childNodes[0].data + "\t"
            
            entryString += str(adjustedAltitudeAngleStr)
            
#             entryString += self.adjustedAltitude(sighting.getElementsByTagName("time")[0].childNodes[0].data)
            
            print entryString
            entryString = ""
            
        self.EndOfLog()
        
        return (self.approximateLatitude, self.approximateLongitude)

# private
    def FahrenheitToCelsius(self, fahrenheit):
        celsius = (float(fahrenheit) - 32 ) / 1.8
        return celsius

# private
    def adjustedAltitude(self, altitude = 0):
        return "0d0.0"


#     private    
    def startOfLog(self):
        print self.entryHeader() + "Start of log"
        print self.entryHeader() + "Start of sighting file: " + self.sightingFile

#     private    
    def EndOfLog(self):
        print self.entryHeader() + "End of sighting file: " + self.sightingFile
    
#     private    
    def entryHeader(self):
        entryHeader = "LOG: " + self.getDateTime() + " "
        return entryHeader
    
#     private
    def getDateTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         return datetime.datetime.now()
    
    
    
    
    
    
    
    
    
    
    
    
    