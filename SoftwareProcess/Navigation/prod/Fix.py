import xml.dom.minidom
import time
import math
import Angle
import os
import re

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
        domTree = xml.dom.minidom.parse(self.sightingFile)
        sightingTree = domTree.documentElement
        sightings = sightingTree.getElementsByTagName("sighting")

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
                    
                    entryString += self.body + "\t"
                    entryString += self.date + "\t"
                    entryString += self.time + "\t"            
                    
                    entryString += str(adjustedAltitudeAngleStr) + "\t"
                    gha = self.getGHA()
                    entryString += gha[0] + "\t" +gha[1] + "\t"
                    
                    self.logFile.write(entryString+"\n")
                    self.logFile.flush()
        
                    entryString = ""
                    
                else:
                    self.sightingErrors+=1
        self.EndOfLog()
        
        return (self.approximateLatitude, self.approximateLongitude)
    
    def setAriesFile(self, ariesFile):
        entryString = ""
        self.ariesFileString = ariesFile
        if(isinstance(ariesFile, str)):
            if(os.path.exists(ariesFile)):
                try:
                    self.ariesFile = open(ariesFile)
                except:
                    raise ValueError()
                self.ariesAbsoluteFilePath = os.path.abspath(ariesFile)
                entryString = "Aries file:\t" + self.ariesAbsoluteFilePath
                self.writeEntry(entryString)
                self.ariesFile.close()
                return self.ariesAbsoluteFilePath
                
    
    def setStarFile(self, starFile):
        entryString = ""
        self.starFileString = starFile
        if(isinstance(starFile, str)):
            if(os.path.exists(starFile)):
                try:
                    self.starFile = open(starFile)
                except:
                    raise ValueError()
                self.starAbsoluteFilePath = os.path.abspath(starFile)
                entryString = "Star file:\t" + self.starAbsoluteFilePath
                self.writeEntry(entryString)
                self.starFile.close()
                return self.starAbsoluteFilePath

    def getGHA(self):
        star = self.readStars()
        if star is not None:
            starSHAString = star['longitude']
            geographicPositionLatitude = star['latitude']
            starSHAangle = Angle.Angle()
            starSHAangle.setDegreesAndMinutes(starSHAString)
            starSHA = starSHAangle.getDegrees()
            aries = self.readAries()
            if aries == 0:
                return ("0d0.0", "0d0.0")
            if not aries is None:
                aries1GHA = Angle.Angle()
                aries2GHA = Angle.Angle()
                aries1GHA.setDegreesAndMinutes(aries[0]['gha'])
                aries2GHA.setDegreesAndMinutes(aries[1]['gha'])
                
                timeArray = self.time.split(":")
                s = float(timeArray[1]) * 60 + float(timeArray[2])
                
                m = aries2GHA.subtract(aries1GHA)* (s / 3600)
                
                ariesGHA = aries1GHA.getDegrees() + m

                observationGHA = ariesGHA + starSHA
                observationGHAAngle = Angle.Angle()
                observationGHAAngle.setDegrees(observationGHA)
                geographicPositionLongitude = observationGHAAngle.getString()
                return (geographicPositionLatitude, geographicPositionLongitude)
            
            
        
    def readAries(self):
        self.ariesFile = open(self.ariesFileString)
        ariesFileEntries = self.ariesFile.readlines()
        ariesEntryDic1={}
        tag = 0
        for ariesFileEntry in ariesFileEntries:
            ariesFileLineArray = ariesFileEntry.split()
            date1 = time.strptime(self.date, "%Y-%m-%d")
            time1Array = self.time.split(":")
            time1 = int(time1Array[0])
            date2 = time.strptime(ariesFileLineArray[0], "%m/%d/%y")
            time2 = int(ariesFileLineArray[1])
            
            if tag == 1:
                ariesEntryDic2 = {'date': ariesFileLineArray[0],
                             'hour': ariesFileLineArray[1],
                             'gha': ariesFileLineArray[2]}
                return ariesEntryDic1, ariesEntryDic2
            
            if date1 == date2 and time1 == time2:
                if tag == 0:
                    ariesEntryDic1 = {'date': ariesFileLineArray[0],
                                 'hour': ariesFileLineArray[1],
                                 'gha': ariesFileLineArray[2]}
                    tag = tag + 1
            
        if tag == 0:
            return 0
            
            
           
    
    def readStars(self):
        if self.starFileString == "":
            raise ValueError("Fix.readStars:")
        else:
            self.starFile = open(self.starFileString)
            starFileEntries = self.starFile.readlines()
            starEntryDic = {'body': '', 'date': '', 'longitude': '','latitude':'' }
            loopTime = 0
            for starFileEntry in starFileEntries:
                starFileLineArray = starFileEntry.split()
                if(starFileLineArray[0] == self.body):
                    date1 = time.strptime(self.date, "%Y-%m-%d")
                    date2 = time.strptime(starFileLineArray[1], "%m/%d/%y")
                    if date1>date2 or loopTime == 0:
                        starEntryDic = {'body': starFileLineArray[0], 
                         'date': starFileLineArray[1],
                         'longitude': starFileLineArray[2],
                         'latitude': starFileLineArray[3]}
                        loopTime += 1
                    else:
                        return starEntryDic

#private
    def handleDomTree(self, sighting):
        timeStr = "^(?P<hour>[0-2]?[0-3]):(?P<minute>[0-5]?[0-9]):(?P<second>[0-5]?[0-9])$"
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
        if self.horizon == "Natural":
            self.height = float(self.height)
            dip = (-0.97 * math.sqrt(self.height)) / 60
        else:
            dip = 0
            
        refraction = (-0.00452 * float(self.pressure)) / (273 + self.FahrenheitToCelsius(self.temperature)) / math.atan(self.observation)
        
        adjustedAltitude = self.observation + dip + refraction
        return adjustedAltitude

#     private    
    def startOfLog(self):
#         self.logFile.write(self.entryHeader() + "Start of log" + "\n")
        self.logFile.write(self.entryHeader() + "Log file:\t" + self.logAbsoluteFilePath + "\n")
        self.logFile.flush()

    def startOfSightingFile(self):
        self.logFile.write(self.entryHeader() + "Sighting file:\t" +self.absoluteSightingFilePath +"\n")
        self.logFile.flush()

#     private    
    def EndOfLog(self):
        self.logFile.write(self.entryHeader() + "Sighting errors: " + str(self.sightingErrors) +"\n")
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
