import xml.dom.minidom
import time
import math
import Angle
import os
import re
from datetime import datetime

class Fix(object):

    def __init__(self, logFile = 'log.txt'):
        functionName = "Fix.__init__: "
        self.starFileString = ""
        self.sightingErrors = 0
        if not isinstance(logFile, basestring):
            raise ValueError(functionName + "logFile must be a String!")
        if len(logFile) < 1:
            raise ValueError(functionName)
        self.logFile = logFile
        self.logFileString = logFile
        self.sightingFile = ""
        self.approximateLatitude = "0d0.0"
        self.approximateLongitude = "0d0.0"
        try:
            self.logFile = open(logFile,'r')
        except IOError:
            self.logFile = open(logFile, 'w')
        else:
            self.logFile = open(logFile,'a')
        
        self.logAbsoluteFilePath = os.path.abspath(self.logFileString)
        self.startOfLog()
        
        self.body = None
        self.date = None
        self.time = None
        self.observation = None
        self.height = None
        self.temperature = None
        self.pressure = None
        self.horizon = None

    def setSightingFile(self, sightingFile = 0):
        if sightingFile is 0:
            raise ValueError('Fix.setSightingFile:')
        self.sightingFile = sightingFile
        self.sightingFileString = sightingFile
        
        if isinstance(sightingFile, int) or isinstance(sightingFile, float):
            raise ValueError('Fix.setSightingFile:')
        
        if os.path.exists(sightingFile):
            self.absoluteSightingFilePath = os.path.abspath(self.sightingFileString)
        else:
            raise ValueError('Fix.setSightingFile:')
        if not os.path.realpath(self.absoluteSightingFilePath):
            raise ValueError('Fix.setSightingFile:')
        if ".xml" not in sightingFile:
            raise ValueError('Fix.setSightingFile:')
        sightingFileArray = sightingFile.split(".")
        if sightingFileArray[0] == "":
            raise ValueError('Fix.setSightingFile:')
        
        self.startOfSightingFile()
        try:
            open(sightingFile, 'r')
            return sightingFile
        except:
            raise ValueError('Fix.setSightingFile:')
            return sightingFile
            
    def getSightings(self):
        if self.sightingFile == "":
            raise ValueError('Fix.getSightings:')
        entryString = ""
        xmlFile = open(self.sightingFile)
        xmlFileLines = xmlFile.readlines()
        xmlFileString = ""
        for xmlFileLine in xmlFileLines:
            xmlFileString += xmlFileLine
        domTree = xml.dom.minidom.parseString(xmlFileString)
        domTree.toprettyxml()
        sightingTree = domTree.documentElement
        sightings = sightingTree.getElementsByTagName("sighting")
        
        entryLists = []
        for sighting in sightings:
            resultHandle = self.handleDomTree(sighting)
            if resultHandle == 0:
                raise ValueError('Fix.getSightings:')
            else:
                if not self.body == "Unknown":
                    entryString = self.entryHeader()
                    
                     
                    adjustedAltitude = self.calculateAdjustedAltitude()
                    
                    adjustedAltitudeAngle = Angle.Angle()
                    adjustedAltitudeAngle.setDegrees(adjustedAltitude)
                    adjustedAltitudeAngleStr = adjustedAltitudeAngle.getString()
                    myDatetime = datetime.strptime(self.date+' '+self.time, "%Y-%m-%d %H:%M:%S")
                    entryDic = {'body':self.body, 'datetime':myDatetime, 'adjustedAltitude': adjustedAltitudeAngleStr}
                    entryLists.append(entryDic)                    
                else:
                    self.sightingErrors+=1
        
        i = 0
        j = 0
        lenOfEntry = len(entryLists)
        for i in range(lenOfEntry-1):
            for j in range(lenOfEntry-1):
                if entryLists[j]['datetime']>entryLists[j+1]['datetime']:
                    tempList = entryLists[j]
                    entryLists[j] = entryLists[j+1]
                    entryLists[j+1] = tempList
                j += 1
            i += 1
            
        for entryDic in entryLists:
            entryString = entryDic['body']+"\t" + str(entryDic['datetime']) +"\t"+entryDic['adjustedAltitude']
            self.writeEntry(entryString)
            
        self.EndOfLog()
        
        return (self.approximateLatitude, self.approximateLongitude)

#private
    def handleDomTree(self, sighting):
        timeStr = "^(?P<hour>[0-1]?[0-9]|[2][0-3]):(?P<minute>[0-5]?[0-9]):(?P<second>[0-5]?[0-9])$"
        dateStr = "^(?P<year>[0-9]{4})\-(?P<month>[0-3]?[0-9])\-(?P<day>[0-3]?[0-9])$"
        
        if len(sighting.getElementsByTagName("body")) is not 0:
            if len(sighting.getElementsByTagName("body")[0].childNodes) is not 0:              
                self.body = sighting.getElementsByTagName("body")[0].childNodes[0].data
            else:
                return 0
        else:
            return 0
        
        self.date = sighting.getElementsByTagName("date")[0].childNodes[0].data
        
        if len(sighting.getElementsByTagName("date")) is not 0:
            if len(sighting.getElementsByTagName("date")[0].childNodes) is not 0:
                self.date = sighting.getElementsByTagName("date")[0].childNodes[0].data
                isDate = re.search(dateStr, self.date)
                if not isDate:
                    return 0
        
        if len(sighting.getElementsByTagName("time")) is not 0:
            if len(sighting.getElementsByTagName("time")[0].childNodes) is not 0:
                self.time = sighting.getElementsByTagName("time")[0].childNodes[0].data
                isTime = re.search(timeStr, self.time)
                if not isTime:
                    return 0
                
        
        self.observation = sighting.getElementsByTagName("observation")[0].childNodes[0].data
        observationTestAngle = Angle.Angle()
        try:
            observationTestAngle.setDegreesAndMinutes(self.observation)
        except:
            return 0
        
        altitudeAngle = Angle.Angle()
        self.observation = altitudeAngle.setDegreesAndMinutes(self.observation)
        
        if len(sighting.getElementsByTagName("height")) is not 0:
            if len(sighting.getElementsByTagName("height")[0].childNodes) is not 0:
                self.height = sighting.getElementsByTagName("height")[0].childNodes[0].data
                try:
                    float(self.height)
                except:
                    isFloat = False
                else:
                    isFloat = True
                if not isFloat:
                    return 0
            else:
                self.height = 0.0
        else:
            self.height = 0.0

        if len(sighting.getElementsByTagName("temperature")) is not 0:
            if len(sighting.getElementsByTagName("temperature")[0].childNodes) is not 0:
                self.temperature = float(sighting.getElementsByTagName("temperature")[0].childNodes[0].data)
                try:
                    int(self.temperature)
                except:
                    isTemperature = False
                else:
                    if self.temperature <=120 and self.temperature >=-20:
                        isTemperature = True
                    else:
                        isTemperature = False
                if not isTemperature:
                    return 0
            else:
                self.temperature = 72.0
        else:
            self.temperature = 72.0
        
            
        if len(sighting.getElementsByTagName("pressure")) is not 0:
            if not len(sighting.getElementsByTagName("pressure")[0].childNodes) == 0:
                self.pressure = sighting.getElementsByTagName("pressure")[0].childNodes[0].data
                try:
                    int(self.pressure)
                except:
                    isPressure = False
                else:
                    self.pressure = int(self.pressure)
                    if self.pressure <=1100 and self.pressure >=100:
                        isPressure = True
                    else:
                        isPressure = False
                if not isPressure:
                    return 0
                
            else:
                self.pressure = 1010
        else:
            self.pressure = 1010
        
        if len(sighting.getElementsByTagName("horizon")) is not 0:
            if not len(sighting.getElementsByTagName("horizon")[0].childNodes) == 0:
                self.horizon = sighting.getElementsByTagName("horizon")[0].childNodes[0].data
                if not (self.horizon == 'Artificial' or 
                        self.horizon =='Natural' or 
                        self.horizon =='artificial' or 
                        self.horizon =='natural'):
                    return 0
            else:
                self.horizon = "Natural"
        else:
            self.horizon = "Natural"
        
        return 1

# private
    def FahrenheitToCelsius(self, fahrenheit):
        celsius = (float(fahrenheit) - 32 ) / 1.8
        return celsius

# private
    def adjustedAltitude(self, altitude = 0):
        return "0d0.0"
#private
    def calculateAdjustedAltitude(self):
        if self.horizon == "Natural" or self.horizon == "natural":
            self.height = float(self.height)
            dip = (-0.97 * math.sqrt(self.height)) / 60
        else:
            dip = 0

        refraction = (-0.00452 * float(self.pressure)) / (273 + self.FahrenheitToCelsius(self.temperature)) / math.tan((math.pi * float(self.observation))/180.0)
        
        adjustedAltitude = self.observation + dip + refraction
        return adjustedAltitude

#     private    
    def startOfLog(self):
        self.logFile.write(self.entryHeader() + "Start of log" + "\n")
        self.logFile.flush()

    def startOfSightingFile(self):
        self.logFile.write(self.entryHeader() + "Start of sighting file: " +self.sightingFileString +"\n")
        self.logFile.flush()

#     private    
    def EndOfLog(self):
        self.logFile.write(self.entryHeader() + "End of sighting file: " + self.sightingFileString +"\n")
        self.logFile.flush()
        self.logFile.close()
    
#     private    
    def entryHeader(self):
        entryHeader = "LOG: " + self.getDateTime() + " "
        return entryHeader
    
    def writeEntry(self, entry):
        self.logFile.write(self.entryHeader() + entry +"\n")
        self.logFile.flush()
#     private
    def getDateTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
