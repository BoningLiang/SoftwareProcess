import xml.dom.minidom
import time
import math
import Angle
import os
import re
from __builtin__ import str

class Fix(object):

    def __init__(self, logFile = 'log.txt'):
        functionName = "Fix.__init__: "
        self.starFileString = ""
        
        self.settedAriesFile = 0
        self.settedStarsFile = 0
        
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
        self.returnApproximateLatitude = "0d0.0"
        self.returnApproximateLongitude = "0d0.0"
        
        self.starFileString = "stars.txt"
        self.ariesFileString = "aries.txt"
        
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
        except:
            raise ValueError('Fix.setSightingFile:')
        return self.absoluteSightingFilePath
            
    def getSightings(self, assumedLatitude = "0d0.0", assumedLongitude = "0d0.0"):
        
#         assumedLatitudeDegree = self.dealAssumedLatitude(assumedLatitude)
        assumedLatitudeAngle = self.dealAssumedLatitude(assumedLatitude)
        assumedLongitudeAngle = self.dealAssumedLongitude(assumedLongitude)
        if assumedLatitudeAngle == 0:
            raise ValueError("Fix.getSightings:")
        if assumedLongitudeAngle == 0:
            raise ValueError("Fix.getSightings:")
        
        
        if self.settedAriesFile == 0 or self.settedStarsFile == 0:
            raise ValueError('Fix.getSightings:')
        
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
        
        sumCosForEachSighting=0
        sumSinForEachSighting=0
        
        for sighting in sightings:
            resultHandle = self.handleDomTree(sighting)
            if resultHandle == 0:
                self.sightingErrors+=1
#                 raise ValueError('Fix.getSightings:')
            else:
                if not self.body == "Unknown":
                    entryString = self.entryHeader()
                     
                    adjustedAltitude = self.calculateAdjustedAltitude()
                    
                    adjustedAltitudeAngle = Angle.Angle()
                    adjustedAltitudeAngle.setDegrees(adjustedAltitude)
                    adjustedAltitudeAngleStr = adjustedAltitudeAngle.getString()
                    adjustedAltitudeDegree = adjustedAltitudeAngle.getDegrees()
                    
#                     print "adjusted altitude: " + adjustedAltitudeAngleStr
                    
                    entryString += self.body + "\t"
                    entryString += self.date + "\t"
                    entryString += self.time + "\t"            
                    
                    entryString += str(adjustedAltitudeAngleStr) + "\t"
                    gha = self.getGHA()
                    
                    geographicPositionLatitudeAngle = Angle.Angle()
                    geographicPositionLongitudeAngle = Angle.Angle()
                    
                    geographicPositionLatitudeAngle.setDegreesAndMinutes(gha[0])
                    geographicPositionLongitudeAngle.setDegreesAndMinutes(gha[1])
                    
#                     print "geographic position altitude: " + gha[0]
#                     print "geographic position longitude: " + gha[1]
                    
                    geographicPositionLatitudeDegree = geographicPositionLatitudeAngle.getDegrees()
                    geographicPositionLongitudeDegree = geographicPositionLongitudeAngle.getDegrees()
                    
                    entryString += gha[0] + "\t" +gha[1] + "\t"
                    entryString += assumedLatitude + "\t" + assumedLongitude +"\t"
                    #azimuth and distance
                    #A Calculate local hour angle LHA
                    LHAAngle = Angle.Angle()
                    LHAAngle.setDegrees(geographicPositionLongitudeDegree)
                    LHAAngle.add(assumedLongitudeAngle)
                    LHA = LHAAngle.getDegrees()
                    
                    #B Calculate the angle by which to ....
                    sinLat1 = math.sin(math.radians(geographicPositionLatitudeAngle.getDegrees()))
                    print "sinLat1: "+str(sinLat1)
                    sinLat2 = math.sin(math.radians(assumedLatitudeAngle.getDegrees()))
                    print "sinLat2: "+str(sinLat2)
                    sinLat = sinLat1 * sinLat2
                    print "sinLat: "+str(sinLat)
                    
                    cosLat1 = math.cos(math.radians(geographicPositionLatitudeAngle.getDegrees()))
                    print "cosLat1: "+str(cosLat1)
                    cosLat2 = math.cos(math.radians(assumedLatitudeAngle.getDegrees()))
                    print "cosLat2: "+str(cosLat2)
                    cosLHA = math.cos(math.radians(LHA))
                    print "cosLHA: "+str(cosLHA)
                    cosLat = cosLat1 * cosLat2 * cosLHA
                    print "cosLat: "+str(cosLat)
                    intermediateDistance = sinLat + cosLat
                    print "intermediateDistance: "+ str(intermediateDistance)
                    correctedAltitude = math.asin(intermediateDistance)
                    print "correctedAltitude: " +str(correctedAltitude) 
                    
                    #C
                    distanceAdjustmentFloat = 60*(math.degrees(correctedAltitude) - adjustedAltitudeDegree)
                    distanceAdjustmentInteger = round(distanceAdjustmentFloat)
                    print "distance adjustment (before round): "+str(distanceAdjustmentFloat), "*"*30 , "distance"
                    print "distance adjustment: "+str(distanceAdjustmentInteger), "*"*30 , "distance"
                    
                    #D
                    print "D: =================================="
                    theNumerator = sinLat1 - sinLat2 * intermediateDistance
                    print "numerator: "+str(theNumerator)
                    cosLat1 = math.cos(math.radians(assumedLatitudeAngle.getDegrees()))
                    print "cosLat1: "+str(cosLat1)
                    cosLat2 = math.cos(correctedAltitude)
                    print "cosLat2: "+str(cosLat2)
                    theDenominator = cosLat1 * cosLat2
                    print "denominator: "+str(theDenominator)
                    intermediaAzimuth = theNumerator / theDenominator
                    print "intermedia azimuth: "+str(intermediaAzimuth)
                    azimuthAdjustment = math.acos(intermediaAzimuth)
                    print "azimuth adjustment(rad): "+str(azimuthAdjustment)
                    azimuthAdjustmentAngle = Angle.Angle()
                    
                    azimuthAdjustmentAngle.setDegrees(math.degrees(azimuthAdjustment))
                    
                    print "azimuth adjustment: "+azimuthAdjustmentAngle.getString(), "*"*30 , "azimuth"
                    entryString += azimuthAdjustmentAngle.getString() + "\t" + str(distanceAdjustmentInteger) +"\t"               
                    
                    
                    sumCosForEachSighting += distanceAdjustmentInteger * math.cos(math.radians(azimuthAdjustmentAngle.getDegrees()))
                    
                    sumSinForEachSighting += distanceAdjustmentInteger * math.sin(math.radians(azimuthAdjustmentAngle.getDegrees()))
                    
                    self.logFile.write(entryString+"\n")
                    self.logFile.flush()
        
                    entryString = ""
                    
                else:
                    self.sightingErrors+=1
        
        print "\n"
        print "distance adjustment * cos(azimuth adjustment) = "+ str(sumCosForEachSighting)
        print "distance adjustment * sin(azimuth adjustment) = "+ str(sumSinForEachSighting)
            
        self.approximateLatitude = assumedLatitudeAngle.getDegrees() + sumCosForEachSighting / 60
        print "assumedLatitudeAngle.getDegrees() = "+str(assumedLatitudeAngle.getDegrees())
        print "sumCosForEachSighting / 60 = "+str(sumCosForEachSighting / 60)
        
        if self.approximateLatitude>=270 and self.approximateLatitude<=360:
            self.approximateLatitude = self.approximateLatitude - 360
        
        if self.approximateLatitude>90 and self.approximateLatitude<270:
            self.approximateLatitude = 180 - self.approximateLatitude
        
        self.approximateLongitude = assumedLongitudeAngle.getDegrees() + sumSinForEachSighting / 60
        
        approximateLatitudeString = str(int(self.approximateLatitude))+"d"+ str(abs(round((self.approximateLatitude-int(self.approximateLatitude))*60,1)))
        if self.approximateLatitude<0:
            approximateLatitudeString = approximateLatitudeString.replace("-","S")
        else:
            approximateLatitudeString = "N" + approximateLatitudeString
        
        approximateLongitudeAngle = Angle.Angle()
        approximateLongitudeAngle.setDegrees(self.approximateLongitude)
        self.returnApproximateLatitude = approximateLatitudeString
        self.returnApproximateLongitude = approximateLongitudeAngle.getString()
        self.EndOfLog()
        return (self.returnApproximateLatitude, self.returnApproximateLongitude)
    
    def setAriesFile(self, ariesFile = 0):
        if ariesFile is 0:
            raise ValueError('Fix.setAriesFile:')
        
        entryString = ""
        self.ariesFileString = ariesFile
        
        if isinstance(ariesFile, int) or isinstance(ariesFile, float):
            raise ValueError('Fix.setAriesFile:')
        
        
        if ".txt" not in ariesFile:
            raise ValueError('Fix.setAriesFile:')
        ariesFileArray = ariesFile.split(".")
        if ariesFileArray[0] == "":
            raise ValueError('Fix.setAriesFile:')
        
        if(isinstance(ariesFile, str)):
            if(os.path.exists(ariesFile)):
                try:
                    self.ariesFile = open(ariesFile)
                except:
                    raise ValueError("Fix.setAriesFile:")
                self.ariesAbsoluteFilePath = os.path.abspath(ariesFile)
                entryString = "Aries file:\t" + self.ariesAbsoluteFilePath
                self.writeEntry(entryString)
                self.ariesFile.close()
                self.settedAriesFile = 1
                return self.ariesAbsoluteFilePath
            else:
                raise ValueError("Fix.setAriesFile:")
            
                
    
    def setStarFile(self, starFile = 0):
        if starFile == 0:
            raise ValueError('Fix.setStarFile:')
        
        entryString = ""
        self.starFileString = starFile
        
        if isinstance(starFile, int) or isinstance(starFile, float):
            raise ValueError('Fix.setStarFile:')
        
        if ".txt" not in starFile:
            raise ValueError('Fix.setStarFile:')
        starFileArray = starFile.split(".")
        if starFileArray[0] == "":
            raise ValueError('Fix.setStarFile:')

        
        if(isinstance(starFile, str)):
            if(os.path.exists(starFile)):
                try:
                    self.starFile = open(starFile)
                except:
                    raise ValueError("Fix.setStarFile:")
                self.starAbsoluteFilePath = os.path.abspath(starFile)
                entryString = "Star file:\t" + self.starAbsoluteFilePath
                self.writeEntry(entryString)
                self.starFile.close()
                self.settedStarsFile = 1
                return self.starAbsoluteFilePath
            else:
                raise ValueError("Fix.setStarFile:")

    def getGHA(self):
        star = self.readStars()
#         print "star: "+star
        if star is not None:
            starSHAString = star['longitude']
            geographicPositionLatitude = star['latitude']
            starSHAangle = Angle.Angle()
            starSHAangle.setDegreesAndMinutes(starSHAString)
            starSHA = starSHAangle.getDegrees()
            aries = self.readAries()
            if aries == 0:
                print "Fix.getGHA()-1"
                return ("0d0.0", "0d0.0")
            if not aries is None:
                aries1GHA = Angle.Angle()
                
                aries2GHA = Angle.Angle()
                aries1GHA.setDegreesAndMinutes(aries[0]['gha'])
                aries2GHA.setDegreesAndMinutes(aries[1]['gha'])
                print "aries1GHA: "+aries1GHA.getString()
                timeArray = self.time.split(":")
                s = float(timeArray[1]) * 60 + float(timeArray[2])
                
                m = aries2GHA.subtract(aries1GHA)* (s / 3600)
                
                ariesGHA = aries1GHA.getDegrees() + m

                observationGHA = ariesGHA + starSHA
                print "ariesGHA: "+str(ariesGHA)
                print "starSHA: "+str(starSHA)
                observationGHAAngle = Angle.Angle()
                observationGHAAngle.setDegrees(observationGHA)
                geographicPositionLongitude = observationGHAAngle.getString()
                return (geographicPositionLatitude, geographicPositionLongitude)
        print "Fix.getGHA()-error"
         
   
    def dealAssumedLatitude(self, assumedLatitude):
        
        if "-" in assumedLatitude:
            print "Fix.dealAssumedLatitude() - 1"
            return 0
        
        if ("N" not in assumedLatitude) and ("S" not in assumedLatitude):
            if assumedLatitude != "0d0.0":
                print "Fix.dealAssumedLatitude() - 2"
                return 0
        
        if "N" in assumedLatitude:
            assumedLatitude = assumedLatitude.replace("N","")
        if "S" in assumedLatitude:
            assumedLatitude = assumedLatitude.replace("S","-")
        
        if "0d0.0" in assumedLatitude:
            if "N" in assumedLatitude or "S" in assumedLatitude:
                print "Fix.dealAssumedLatitude() - 3"
                return 0
        
        assumedLatitudeAngle = Angle.Angle()
        try:
            assumedLatitudeAngle.setDegreesAndMinutes(assumedLatitude)
        except:
            print "Fix.dealAssumedLatitude() - 4"
            return 0
        assumedLatitudeArray = assumedLatitude.split("d")
        print "assumedLatitudeArray[0] = "+assumedLatitudeArray[0]
        if float(assumedLatitudeArray[0])>=90 or float(assumedLatitudeArray[0])<=-90:
            print "Fix.dealAssumedLatitude() - 5"
            return 0
        
        return assumedLatitudeAngle
    
    def dealAssumedLongitude(self, assumedLongitude):
        
        assumedLongitudeAngle = Angle.Angle()
        try:
            assumedLongitudeAngle.setDegreesAndMinutes(assumedLongitude)
        except:
            return 0
        
        return assumedLongitudeAngle
            
        
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
                
                if len(starFileLineArray)>4:
                    for i in range(1,len(starFileLineArray)-3):
                        starFileLineArray[0] = starFileLineArray[0] +" "+ starFileLineArray[i]
#                         print "starFileArray[0] = " + starFileLineArray[0]
                    for i in range(len(starFileLineArray)-4, len(starFileLineArray)-1):
                        starFileLineArray[i] = starFileLineArray[i+1]
                
                starFileLineArray[0] = starFileLineArray[0].strip()
                
                
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
            print "Fix.readStars() - error"

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
        if self.horizon == "natural" or self.horizon == "Natural":
            self.height = float(self.height)
            dip = (-0.97 * math.sqrt(self.height)) / 60
        else:
            dip = 0
            
#         refraction = (-0.00452 * float(self.pressure)) / (273 + self.FahrenheitToCelsius(self.temperature)) / math.tan((math.pi * float(self.observation))/180.0)
        refraction = (-0.00452 * float(self.pressure)) / (273 + self.FahrenheitToCelsius(self.temperature)) / math.tan(math.radians(self.observation))
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
        self.logFile.write(self.entryHeader() + "Sighting errors:\t" + str(self.sightingErrors) +"\n")
        self.logFile.write(self.entryHeader()+"Approximate latitude:\t"+str(self.returnApproximateLatitude)+"\tApproximate longitude:\t"+str(self.returnApproximateLongitude))
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
