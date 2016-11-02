import unittest
import uuid
import os
import Navigation.prod.Fix as F

class TestFix(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.className = "Fix."
        cls.logStartString = "Start of log"
        cls.logSightingString = "Start of sighting file"
        cls.DEFAULT_LOG_FILE = "log.txt"
        
    def setUp(self):
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE) 
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        self.deleteNamedLogFlag = False
    
    def tearDown(self):
        if(self.deleteNamedLogFlag):
            try:
                if(os.path.isfile(self.RANDOM_LOG_FILE)):
                    os.remove(self.RANDOM_LOG_FILE)  
            except:
                pass
        
        
        
# 100 Constructor
#    Analysis
#        inputs:
#            logFile: string, optional, unvalidated, len >= 1
#        outputs:
#            returns:  instance of Fix
#            also:    writes "Start of log" to log file
#
#    Happy tests:
#        logFile:  
#            omitted  -> Fix()
#            new logfile  -> Fix("randomName.txt")
#            existing logfile  -> Fix("myLog.txt") (assuming myLog.txt exits)
#    Sad tests:
#        logFile:
#            nonstring -> Fix(42)
#            length error -> Fix("")
#            
    def test100_010_ShouldConstructFix(self):
        'Fix.__init__'
        self.assertIsInstance(F.Fix(), F.Fix, 
                              "Major error:  Fix not created")
         
    def test100_020_ShouldConstructFixWithDefaultFile(self):
        theFix = F.Fix()
        try:
            theLogFile = open(self.DEFAULT_LOG_FILE, 'r')
            entry = theLogFile.readline()
            self.assertNotEquals(-1, entry.find("Start of log"), 
                                 "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, F.Fix, 
                              "Major:  log file failed to create")
        
    def test100_025_ShouldConstructWithKeywordParm(self):
        try:
            theFix = F.Fix(logFile=self.RANDOM_LOG_FILE)
            self.assertTrue(True)
        except Exception as e:
            self.fail("Major: " + str(e))
        self.deleteNamedLogFlag = True
  
    def test100_030_ShouldConstructFixWithNamedFile(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
            entry = theLogFile.readline()
            del theLogFile
            self.assertNotEquals(-1, entry.find(self.logStartString), 
                                 "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, F.Fix, "Major:  log file failed to create")
        self.deleteNamedLogFlag = True
        
    def test100_040_ShouldConstructFixWithExistingFile(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
            numberOfExpectedEntries = 2
            for _ in range(numberOfExpectedEntries):
                entry = theLogFile.readline()
                self.assertNotEquals(-1, entry.find(self.logStartString), 
                                     "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, F.Fix, 
                              "Major:  log file failed to create")
        self.deleteNamedLogFlag = True
        
    def test100_910_ShouldRaiseExceptionOnFileNameLength(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            F.Fix("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)], 
                          "Minor:  failure to check for log file name length")  
        
    def test100_920_ShouldRaiseExceptionOnNonStringFile(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            F.Fix(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)], 
                          "Minor:  failure to check for non-string log file name")  
        
        
# 200 setSightingFile
#    Analysis
#        inputs:
#            sightingFile: string, mandatory, unvalidated, format = f.xml (len(f) >= 1)
#        outputs:
#            returns:  string with file name
#            also:    writes "Start of sighting file f.xml" to log file
#
#    Happy tests:
#        sightingFile:  
#            legal file name  -> setSightingFile("sightingFile.xml")  
#    Sad tests:
#        sightingFile:
#            nonstring -> setSightinghFile(42)
#            length error -> setSightingFile(".xml")
#            nonXML -> setSightingFile("sightingFile.txt")
#            missing -> setSightingFile()
#            nonexistent file -> setSightingFile("missing.xml")
    def test200_010_ShouldConstructWithKeywordParm(self):
        'Minor:  '
        theFix = F.Fix(logFile=self.RANDOM_LOG_FILE)
        try:
            result = theFix.setSightingFile("CA02_200_ValidStarSightingFile.xml")
            self.assertEquals(result, "CA02_200_ValidStarSightingFile.xml")
        except:
            self.fail("Minor: incorrect keyword specified in setSighting parm")
        self.deleteNamedLogFlag = True 

    def test200_020_ShouldSetValidSightingFile(self):
        theFix = F.Fix()
        result = theFix.setSightingFile("CA02_200_ValidStarSightingFile.xml")
        self.assertEquals(result,"CA02_200_ValidStarSightingFile.xml")
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(self.logSightingString), 
                             "Minor:  first setSighting logged entry is incorrect")
        theLogFile.close()
        
    def test200_910_ShouldRaiseExceptionOnNonStringFileName(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string sighting file name")  
        
    def test200_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(".xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 sighting file name") 
        
    def test200_930_ShouldRaiseExceptionOnNonXmlFile1(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("sighting.")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non.xml sighting file extension")
        
    def test200_940_ShouldRaiseExceptionOnNonXmlFile2(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between sighting file name and extension") 
        
    def test200_950_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing sighting file")       
        
           
    def test200_960_SholdRaiseExceptionOnMissingFile(self):
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(self.RANDOM_LOG_FILE+".xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing sighting file") 
        
# 300 getSightings
#    Analysis
#        inputs:
#            via parm:  none
#            via file:  xml description of sighting
#        outputs:
#            returns:    ("0d0.0", "0d0.0")
#            via file:    writes body /t date /t time /t adjusted altitude in sorted order
#        entry criterion:
#            setSightingsFile must be called first
#
#    Happy tests:
#        sighting file 
#            valid file with any sightings -> should return ("0d0.0", "0d0.0")
#            valid file with mixed indentation -> should not indicate any errors
#            valid file with one sighting  -> should log one star body
#            valid file with multiple sightings -> should log star bodies in sorted order
#            valid file with multiple sightings at same date/time -> should log star bodies in order sorted by body 
#            valid file with zero sightings -> should not log any star bodies
#            valid file with extraneous tag -> should log star(s) without problem
#        sighting file contents
#            valid body with natural horizon -> should calculate altitude with dip
#            valid body with artificial horizon -> should calculate altitude without dip
#            valid body with default values -> should calculate altitude with height=0, temperature=72, pressure=1010, horizon-natural
#    Sad tests:
#        sightingFile:
#            sighting file not previously set
#            sighting file with invalid mandatory tag (one of each:  fix, body, date, time, observation)
#            sighting file with invalid tag value (one of each:  date, time, observation, height, temperature, pressure, horizon)

    def test300_010_ShouldIgnoreMixedIndentation(self):
        testFile = "CA02_300_GenericValidStarSightingFile.xml"
        expectedResult = ("0d0.0", "0d0.0")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        result = theFix.getSightings()
        self.assertTupleEqual(expectedResult, result, 
                              "Minor:  incorrect return value from getSightings")

    def test300_020_ShouldIgnoreMixedIndentation(self):
        testFile = "CA02_300_ValidWithMixedIndentation.xml"
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        try:
            theFix.getSightings()
            self.assertTrue(True)
        except:
            self.fail("Major: getSightings failed on valid file with mixed indentation")  

    def test300_030_ShouldLogOneSighting(self):
        testFile = "CA02_300_ValidOneStarSighting.xml"
        targetStringList = ["Aldebaran", "2016-03-01", "23:40:01"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Log entry is not correct for getSightings")
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True
        
    def test300_040_ShouldLogMultipleSightingsInTimeOrder(self):       
        testFile = "CA02_300_ValidMultipleStarSighting.xml"
        targetStringList = [
            ["Sirius", "2016-03-01", "00:05:05"],
            ["Canopus", "2016-03-02", "23:40:01"]
            ]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
            "Major: failure to find " + targetStringList[0][0] +  " in log")
     
        for targetString in targetStringList:
            if not (targetString[0] in logFileContents[entryIndex]):
                self.fail("failure to find {} in log".format(targetString[0]))
            entryIndex += 1
     
        self.deleteNamedLogFlag = True  
        
    def test300_050_ShouldLogMultipleSightingsWithSameDateTime(self):       
        testFile = "CA02_300_ValidMultipleStarSightingSameDateTime.xml"
        targetStringList = [
            ["Acrux", "2016-03-01", "00:05:05"],
            ["Sirius", "2016-03-01", "00:05:05"],
            ["Canopus", "2016-03-02", "23:40:01"]
            ]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "Major: failure to find " + targetStringList[0][0] +  " in log")
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index][0] in logFileContents[entryIndex])):
                self.fail("Major: failure to find star in log")
        self.deleteNamedLogFlag = True 

    def test300_060_ShouldHandleNoSightings(self):       
        testFile = "CA02_300_ValidWithNoSightings.xml"
        targetString1 = "End of sighting file"
        targetString2 = "Start of sighting file"
        
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        endOfSightingFileIndex = self.indexInList(targetString1, logFileContents)
        self.assertLess(-1,endOfSightingFileIndex,
                           "Major: log file does not contain 'end of sighting file' entry")
        self.assertLess(1, endOfSightingFileIndex,
                           "Major: log file does not contain sufficient entries")
        self.assertTrue((targetString2 in logFileContents[endOfSightingFileIndex - 1]))
        self.deleteNamedLogFlag = True 
        
    def test300_070_ShouldIgnoreExtraneousTags(self):       
        testFile = "CA02_300_ValidWithExtraneousTags.xml"
        targetStringList = [
            ["Sirius", "2016-03-01", "00:05:05"],
            ]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "Major: failure to find " + targetStringList[0][0] +  " in log")
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index][0] in logFileContents[entryIndex])):
                self.fail("Major: failure to find star in log")
        self.deleteNamedLogFlag = True


    def test300_080_ShouldLogStarWithNaturalHorizon(self):
        testFile = "CA02_300_ValidOneStarNaturalHorizon.xml"
        targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d55.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Log entry is not correct for getSightings")
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True


    def test300_080_ShouldLogStarWithArtificialHorizon(self):
        testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
        targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d55.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Log entry is not correct for getSightings")
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True
        
        
    def test300_090_ShouldLogStarWithDefaultSightingValues(self):
        testFile = "CA02_300_ValidOneStarWithDefaultValues.xml"
        targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d59.9"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Log entry is not correct for getSightings")
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True

    def test300_910_ShouldRaiseExceptionOnNotSettingSightingsFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()")   
        
    def test300_920_ShouldRaiseExceptionOnMissingMandatoryTag(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidWithMissingMandatoryTags.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing mandatory tag")   
        
    def test300_930_ShouldRaiseExceptionOnInvalidBody(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidBody.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for invalid body")    
        
    def test300_940_ShouldRaiseExceptionOnInvalidDate(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidDate.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for invalid date") 
        
    def test300_950_ShouldRaiseExceptionOnInvalidTime(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidTime.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for invalid time")    
        
    def test300_960_ShouldRaiseExceptionOnInvalidObservation(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidObservation.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for invalid observation")       
        
    def test300_970_ShouldRaiseExceptionOnInvalidHeight(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidHeight.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for invalid height" )
        
    def test300_980_ShouldRaiseExceptionOnInvalidTemperature(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidTemperature.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for invalid temperature" )
        
    def test300_990_ShouldRaiseExceptionOnInvalidPressure(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidPressure.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for invalid pressure" )
        
    def test300_995_ShouldRaiseExceptionOnInvalidHorizon(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("CA02_300_InvalidHorizon.xml")
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for invalid horizon" )
        

#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
    