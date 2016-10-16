import xml.dom.minidom
import time
import math
import Angle

class Fix(object):

    def __init__(self, logFile = 'log.txt'):
        functionName = "Fix.__init__: "

        if not isinstance(logFile, basestring):
            raise ValueError(functionName + "logFile must be a String!")
        
        self.logFile = logFile
        self.logFileString = logFile
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
        
        self.body = None
        self.date = None
        self.time = None
        self.observation = None
        self.height = None
        self.temperature = None
        self.pressure = None
        self.horizon = None

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

        entryString = ""
        domTree = xml.dom.minidom.parse(self.sightingFile)
        sightingTree = domTree.documentElement
        sightings = sightingTree.getElementsByTagName("sighting")

        for sighting in sightings:
            
            self.handleDomTree(sighting)

            entryString = self.entryHeader()
             
            adjustedAltitude = self.calculateAdjustedAltitude()
            
            adjustedAltitudeAngle = Angle.Angle()
            adjustedAltitudeAngle.setDegrees(adjustedAltitude)
            adjustedAltitudeAngleStr = adjustedAltitudeAngle.getString()
            
            entryString += self.body + "\t"
            entryString += self.date + "\t"
            entryString += self.time + "\t"
            
            entryString += str(adjustedAltitudeAngleStr)
            
            self.logFile.write(entryString+"\n")
            self.logFile.flush()

            entryString = ""
            
        self.EndOfLog()
        
        return (self.approximateLatitude, self.approximateLongitude)

#private
    def handleDomTree(self, sighting):
                          
        self.body = sighting.getElementsByTagName("body")[0].childNodes[0].data
        self.date = sighting.getElementsByTagName("date")[0].childNodes[0].data
        self.time = sighting.getElementsByTagName("time")[0].childNodes[0].data
        
        self.observation = sighting.getElementsByTagName("observation")[0].childNodes[0].data
        altitudeAngle = Angle.Angle()
        self.observation = altitudeAngle.setDegreesAndMinutes(self.observation)
        
        if not len(sighting.getElementsByTagName("height")[0].childNodes) == 0:
            self.height = float(sighting.getElementsByTagName("height")[0].childNodes[0].data)
        else:
            self.height = 0
        self.height = float(self.height)

        if not len(sighting.getElementsByTagName("temperature")[0].childNodes) == 0:
            self.temperature = float(sighting.getElementsByTagName("temperature")[0].childNodes[0].data)
        else:
            self.temperature = 72
            
        
        if not len(sighting.getElementsByTagName("pressure")[0].childNodes) == 0:
            self.pressure = float(sighting.getElementsByTagName("pressure")[0].childNodes[0].data)
        else:
            self.pressure = 1010
            
        
        if not len(sighting.getElementsByTagName("horizon")[0].childNodes) == 0:
            self.horizon = sighting.getElementsByTagName("horizon")[0].childNodes[0].data
        else:
            self.horizon = "Natural"

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
            dip = (-0.97 * math.sqrt(self.height)) / 60
        else:
            dip = 0
            
        refraction = (-0.00452 * float(self.pressure)) / (273 + self.FahrenheitToCelsius(self.temperature)) / math.atan(self.observation)
        
        adjustedAltitude = self.observation + dip + refraction
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
        self.logFile.close()
    
#     private    
    def entryHeader(self):
        entryHeader = "LOG: " + self.getDateTime() + " "
        return entryHeader
    
#     private
    def getDateTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
