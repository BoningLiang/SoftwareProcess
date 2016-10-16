import unittest
import Navigation.prod.Fix as F
import os

class FixTest(unittest.TestCase):



    def setUp(self):
        
        try:
            open("existingFile.txt","w")
        except:
            pass
        
        try:
            os.remove("log.txt")
        except:
            pass
        
        try:
            os.remove("myLog.txt")
        except:
            pass
        
        try:
            os.remove("newSighting.xml")
        except:
            pass

    def tearDown(self):
        pass

# -----------------------------------------------------------------------
# ---- Acceptance Tests
# 100 constructor
#    input:    logFile
#    outputs:    instance of Fix
#                writting "Start of log" to log file
#    Happy path:
#        logFile:
#                ommited -> Fix()
#                new LogFile -> Fix("myLog.txt")
#                existing logFile
#    Sad path:
#        logFile:
#                nonString -> Fix(42)
# Happy path 

    def test100_010_ShouldConstructOmmitted(self):
        myFix = F.Fix()
        self.assertIsInstance(myFix, F.Fix)
        try:
            logTxtFile = open("log.txt")
            entryFirstLine = logTxtFile.readline()
            if "Start of log" not in entryFirstLine:
                self.fail()
        except:
            self.fail()
        
        
    def test100_020_ShouldConstructNewLogFile(self):
        self.assertIsInstance(F.Fix("myLog.txt"), F.Fix)
        try:
            logTxtFile = open("myLog.txt")
            entryFirstLine = logTxtFile.readline()
            if "Start of log" not in entryFirstLine:
                self.fail()
        except:
            self.fail()
        
    def test100_030_ShouldConstructExistingLogFile(self):
        self.assertIsInstance(F.Fix("existingFile.txt"), F.Fix)
        try:
            logTxtFile = open("existingFile.txt")
            entryFirstLine = logTxtFile.readline()
            if "Start of log" not in entryFirstLine:
                self.fail()
        except:
            self.fail()
# sad path
    def test100_910_ShouldRaiseExceptionNonString(self):
        expectedString = "Fix.__init__:"
        with self.assertRaises(ValueError) as context:
            F.Fix(43)
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])  
        
# 200 setSightingFile
#    input:    sightingFile    a string of "f.xml"
#    output:    True
#                False
#                write "Start of sighting file f.xml" to the log file
#    
#    happy path:
#        sightingFile:    
#                new file
#                existing file        
#
#
#
# Happy path
    def test200_010_ShouldSetNewSightingFile(self):
        myF = F.Fix()
        self.assertEqual(myF.setSightingFile("newSighting.xml"), True)
        
        try:
            logTxtFile = open("log.txt")
            entryFirstLine = logTxtFile.readline()
            entrySecondLine = logTxtFile.readline()
            if "Start of sighting file: newSighting.xml" not in entrySecondLine:
                self.fail()
        except:
            self.fail()
            
        
    def test200_020_ShouldSetExistingSightingFile(self):
        myF = F.Fix()
        self.assertEqual(myF.setSightingFile("sightingFile.xml"), False)
        
        try:
            logTxtFile = open("log.txt")
            entryFirstLine = logTxtFile.readline()
            entrySecondLine = logTxtFile.readline()
            if "Start of sighting file: sightingFile.xml" not in entrySecondLine:
                self.fail()
        except:
            self.fail()
        
# sad path


# 300 getSightings
#    input:
#    output:
#        a tuple with latitude and longitude
#        write log to log file
#    
#    happy path
#        omitted some attribute in xml
#
# Happy path    
    def test300_010_ShouldReturnLatitudeAndLongitude(self):
        myF = F.Fix()
        myF.setSightingFile("sightingFile.xml")
        self.assertEqual(myF.getSightings(), ("0d0.0","0d0.0"))
        
    def test300_020_ShouldReturnLLWithOmittedAttribute(self):
        myF = F.Fix()
        myF.setSightingFile("sightingOmittedFile.xml")
        self.assertEqual(myF.getSightings(), ("0d0.0","0d0.0"))
        
    

# 400 FahrenheitToCelsius



# Happy path
    def test400_010_ShouldCalculateCelsius(self):
        myF = F.Fix()
        self.assertAlmostEquals(myF.FahrenheitToCelsius(70.0), 21.1111, 3)
          
    def test400_020_ShouldCalculateCelsius(self):
        myF = F.Fix()
        self.assertAlmostEquals(myF.FahrenheitToCelsius(0.0), -17.7777778, 3)
          
    def test400_030_ShouldCalculateCelsius(self):
        myF = F.Fix()
        self.assertAlmostEquals(myF.FahrenheitToCelsius(100.0), 37.7777778, 3)
        


