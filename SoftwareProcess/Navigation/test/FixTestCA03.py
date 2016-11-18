import unittest
import uuid
import os
import Navigation.prod.Fix as F

class TestFix(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.className = "Fix."
        cls.logStartString = "Log file:"
        cls.starSightingString = "Sighting file:"
        cls.starSightingErrorString = "Sighting errors:"
        cls.ariesFileString = "Aries file:"
        cls.starFileString = "Star file:"
        cls.DEFAULT_LOG_FILE = "log.txt"
        cls.ariesFileName = "CA03_Valid_Aries.txt"
        cls.starFileName = "CA03_Valid_Stars.txt"
        cls.testToFileMap = [
            ["validStarSightingFile", "CA02_200_ValidStarSightingFile.xml"],
            ["validAriesFile", "CA03_Valid_Aries.txt"],           
            ["validStarFile", "CA03_Valid_Stars.txt"], 
            ["genericValidStarSightingFile", "CA02_300_GenericValidStarSightingFile.xml"], 
            ["genericValidSightingFileWithMixedIndentation", "CA02_300_ValidWithMixedIndentation.xml"],
            ["validOneStarSighting", "CA02_300_ValidOneStarSighting.xml"],
            ["validMultipleStarSighting", "CA02_300_ValidMultipleStarSighting.xml"],
            ["validMultipleStarSightingSameDateTime", "CA02_300_ValidMultipleStarSightingSameDateTime.xml"],
            ["validWithNoSightings", "CA02_300_ValidWithNoSightings.xml"],
            ["validWithExtraneousTags", "CA02_300_ValidWithExtraneousTags.xml"],
            ["validOneStarNaturalHorizon","CA02_300_ValidOneStarNaturalHorizon.xml"],
            ["validOneStarArtificialHorizon", "CA02_300_ValidOneStarArtificialHorizon.xml"],
            ["validOneStarWithDefaultValues", "CA02_300_ValidOneStarWithDefaultValues.xml"],
            ["invalidWithMissingMandatoryTags","CA02_300_InvalidWithMissingMandatoryTags.xml"],
            ["invalidBodyTag","CA02_300_InvalidBody.xml"],
            ["invalidDateTag","CA02_300_InvalidDate.xml"],
            ["invalidTimeTag","CA02_300_InvalidTime.xml"],
            ["invalidObservationTag","CA02_300_InvalidObservation.xml"],
            ["invalidHeightTag","CA02_300_InvalidHeight.xml"],
            ["invalidTemperatureTag", "CA02_300_InvalidTemperature.xml"],
            ["invalidPressureTag","CA02_300_InvalidPressure.xml"],
            ["invalidHorizonTag","CA02_300_InvalidHorizon.xml"],
            ["validLatLon", "CA03_300_ValidStarLatLon.xml"],
            ["validLatLonInterpolated", "CA03_300_ValidStarLatLonInterpolationRequired.xml"]
            ]  



        
#----------          
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
    
#==================== Fix.__init__ ====================
# 100 Constructor
#    Analysis
#        inputs:
#            logFile: string, optional, unvalidated, len >= 1        regression
#        outputs:
#            returns:  instance of Fix                               regression
#|           also:    writes "Log file: " + filepath of log file     new to CA03
#
#    Happy tests:
#        logFile:  
#            test 010:    omit parm
#            test 020:    construct with default file name        CA03
#            test 030:    construct with named parm                
#            test 040:    construct with specific file name        CA03
#            test 050:    construct and append to existing file
#            existing logfile  -> Fix("myLog.txt") (assuming myLog.txt exits)
#    Sad tests:
#        logFile:
#            test 910:    length error -> Fix("")
#            test 920:    test nonstring -> Fix(42)
#    
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
#----------      
    def test100_010_ShouldConstructFixCA02(self):
        'Construct a Fix ... nothing else'
        self.assertIsInstance(F.Fix(), F.Fix, 
                              "Major error:  Fix not created")

#----------
    def test100_020_ShouldConstructFixWithDefaultFileCA03(self):
        'Construct Fix with default log file name'
        theFix = F.Fix()
        try:
            theLogFile = open(self.DEFAULT_LOG_FILE, 'r')
        except:
            self.fail("Major:  log file failed to create")
        entry = theLogFile.readline()
        theLogFile.close()
        self.assertNotEquals(-1, entry.find(self.logStartString), 
                                 "Minor:  first line of {} is incorrect".format(self.DEFAULT_LOG_FILE))
        self.assertNotEquals(-1, entry.find(self.DEFAULT_LOG_FILE), 
                             "Minor:  first line of log is incorrect")


#----------
    def test100_030_ShouldConstructWithKeywordParmCA02(self):
        'Construct Fix using named parameter'
        try:
            theFix = F.Fix(logFile=self.RANDOM_LOG_FILE)
            self.assertTrue(True)
        except Exception as e:
            self.fail("Minor: " + str(e))
            self.deleteNamedLogFlag = True


#----------
    def test100_040_ShouldWriteFullPathToLogCA03(self):
        'Construct Fix and ensure abspath is written to log file'
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
        except:
            self.fail("Major:  log file failed to create")
        entry = theLogFile.readline()
        theLogFile.close()
        self.assertNotEquals(-1, entry.find(self.RANDOM_LOG_FILE), 
                                 "Major:  first line of log is incorrect " + self.RANDOM_LOG_FILE)
        self.assertNotEquals(-1, entry.find(os.path.abspath(self.RANDOM_LOG_FILE)), 
                                 "Minor:  abspath of log file is not logged " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True
        
 
 #----------
    def test100_050_ShouldConstructFixWithExistingFileCA02(self):
        'Construct Fix and append to existing log file'
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
            numberOfExpectedEntries = 2
            for _ in range(numberOfExpectedEntries):
                entry = theLogFile.readline()
                self.assertNotEquals(-1, entry.find(self.logStartString), 
                                     "Minor:  first line of log is incorrect " + self.RANDOM_LOG_FILE)
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, F.Fix, 
                              "Major:  log file failed to create " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True
        
        
#+++++++++++++++++++ Sad Path Tests ++++++++++++++++++++  
#----------              
    def test100_910_ShouldRaiseExceptionOnFileNameLength(self):
        'Construct Fix with empty string'
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            F.Fix("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)], 
                          "Minor:  failure to check for log file name length")  
#----------   
    def test100_920_ShouldRaiseExceptionOnNonStringFile(self):
        'Construct Fix with invalid parm'
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            F.Fix(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)], 
                          "Minor:  failure to check for non-string log file name")  
    
       
#----------

#==================== Fix.setSightingFile ====================        
# 200 setSightingFile
#    Analysis
#        inputs:
#            sightingFile: string, mandatory, unvalidated, format = f.xml (len(f) >= 1)
#        outputs:
#|            returns:  string with absolute filepath                CA03
#            also:    writes "Sighting file\tf.xml" to log file
#
#    Happy tests:
#        sightingFile:
#            test 010:    legitimate file, no parm name
#            test 020:    legitimate file, named parm  -> verify correct return value                          
#            test 030:    legitimate file name  -> verify correct log 
#    Sad tests:
#        sightingFile:
#            test 910:    nonstring file name
#            test 920:    missing file prefix
#            test 930:    missing .xml file extension
#            test 940:    missing .xml file extension, but presence of "xml" in name
#            test 950:    missing parm
#            test 960:    missing file
#
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
#---------- 
    def test200_010_ShouldSetSightingFileWithOutKeywordParm(self):
        'Set sighting file without keyword parm'
        testFile = self.mapFileToTest("validStarSightingFile")
        theFix = F.Fix()
        try:
            result = theFix.setSightingFile(testFile)
        except Exception as e:
            self.fail("Minor: " + str(e))
        self.assertNotEquals(-1, result.find(testFile), 
                             "Major:  setSightingFile() is not returning file name")
        self.assertNotEquals(-1, result.find(os.path.abspath(testFile)), 
                             "Minor:  setSightingFile() is not returning abspath of file name")

#----------
    def test200_020_ShouldConstructWithKeywordParmCA03(self):
        'Set sighting file with keyword parm'
        testFile = self.mapFileToTest("validStarSightingFile")
        theFix = F.Fix()
        try:
            result = theFix.setSightingFile(sightingFile = testFile)
        except Exception as e:
            self.fail("Minor: " + str(e))
        self.assertNotEquals(-1, result.find(testFile), 
                             "Major:  setSightingFile() is not returning file name")
        self.assertNotEquals(-1, result.find(os.path.abspath(testFile)), 
                             "Minor:  setSightingFile() is not returning abspath of file name")
 
#----------
    def test200_030_ShouldSetValidSightingFile(self):
        'Set sighting file and verify string is written to file'
        testFile = self.mapFileToTest("validStarSightingFile")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        with open(self.DEFAULT_LOG_FILE, "r") as theLogFile:
            logFileContents = theLogFile.readlines()
            self.assertNotEquals(-1, logFileContents[-1].find(self.starSightingString), 
                                 "Major:  correct sighting file string not being logged"),
            self.assertNotEquals(-1, logFileContents[-1].find(os.path.abspath(testFile)),
                                 "Minor:  correct sighting file name not being logged") 
 
 #----------       
    def test200_910_ShouldRaiseExceptionOnNonStringFileName(self):
        'Fail on setting sighting file with non-string name'
        testFile = 42
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string sighting file name")  
   
#----------     
    def test200_920_ShouldRaiseExceptionOnFileLengthError(self):
        'Fail on setting star sighting file with missing file prefix'
        testFile = ".xml"
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 sighting file name") 
#----------      
    def test200_930_ShouldRaiseExceptionOnNonXmlFile1(self):
        'Fail on setting star sighting file with no xml extension'
        testFile = "sighting."
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non xml sighting file extension")

#----------        
    def test200_940_ShouldRaiseExceptionOnNonXmlFile2(self):
        'Fail on setting star sighting file with xml name but not xml extension'
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile("xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between sighting file name and extension") 
 
#----------       
    def test200_950_ShouldRaiseExceptionOnMissingFileName(self):
        'Fail on setting star sighting file with no name'
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing sighting file")       
        
#----------           
    def test200_960_SholdRaiseExceptionOnMissingFile(self):
        'Fail on setting star sighting file that does not exist'
        testFile = self.RANDOM_LOG_FILE+".xml"
        expectedDiag = self.className + "setSightingFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setSightingFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing sighting file") 
        
        
        
#==================== Fix.setAriesFile ====================            
# 400 setAriesFile
#    Analysis
#        inputs:
#            ariesFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  string with absolute filepath                
#            also:    writes "Aries file\tf.txt" to log file
#
#    Happy tests:
#        ariesFile:
#            test 010:    legitimate file, no parm name
#            test 020:    legitimate file, named parm  -> verify correct return value                          
#            test 030:    legitimate file name  -> verify correct log 
#    Sad tests:
#        ariesFile:
#            test 910:    nonstring file name
#            test 920:    missing file prefix
#            test 930:    missing .txt file extension
#            test 940:    missing .txt file extension, but presence of "txt" in name
#            test 950:    missing parm
#            test 960:    missing file
#
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
#---------- 
    def test400_010_ShouldSetAriesFileWithOutKeywordParmCA03(self):
        'Set aries file without keyword parm'
        testFile = self.mapFileToTest("validAriesFile")
        theFix = F.Fix()
        try:
            result = theFix.setAriesFile(testFile)
        except Exception as e:
            self.fail("Minor: " + str(e))
        self.assertNotEquals(-1, result.find(testFile), 
                             "Major:  setAriesFile() is not returning file name")
        self.assertNotEquals(-1, result.find(os.path.abspath(testFile)), 
                             "Minor:  setAriesFile() is not returning abspath of file name")

#----------
    def test400_020_ShouldConstructWithKeywordParmCA03(self):
        'Set aries file with keyword parm'
        testFile = self.mapFileToTest("validAriesFile")
        theFix = F.Fix()
        try:
            result = theFix.setAriesFile(ariesFile = testFile)
        except Exception as e:
            self.fail("Minor: " + str(e))
        self.assertNotEquals(-1, result.find(testFile), 
                             "Major:  setAriesFile() is not returning file name")
        self.assertNotEquals(-1, result.find(os.path.abspath(testFile)), 
                             "Minor:  setAriesFile() is not returning abspath of file name")
 
#----------
    def test400_030_ShouldSetValidAriesFileCA03(self):
        'Set aries file and verify string is written to file'
        testFile = self.mapFileToTest("validAriesFile")
        theFix = F.Fix()
        theFix.setAriesFile(testFile)
        with open(self.DEFAULT_LOG_FILE, "r") as theLogFile:
            logFileContents = theLogFile.readlines()
            self.assertNotEquals(-1, logFileContents[-1].find(self.ariesFileString), 
                                 "Major:  correct aries file string not being logged"),
            self.assertNotEquals(-1, logFileContents[-1].find(os.path.abspath(testFile)),
                                 "Minor:  correct aries file name not being logged") 
 
#----------       
    def test400_910_ShouldRaiseExceptionOnNonStringFileNameCA03(self):
        'Fail on setting aries file with non-string name'
        testFile = 42
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string aries file name")  
   
#----------     
    def test400_920_ShouldRaiseExceptionOnFileLengthErrorCA03(self):
        'Fail on setting aries file with missing file prefix'
        testFile = ".xml"
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 aries file name") 
#----------      
    def test400_930_ShouldRaiseExceptionOnNonXmlFile1CA03(self):
        'Fail on setting aries  file with no txt extension'
        testFile = "aries."
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non txt aries file extension")

#----------        
    def test400_940_ShouldRaiseExceptionOnNonXmlFile2CA03(self):
        'Fail on setting aries  file with txt name but not txt extension'
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between aries file name and extension") 
 
#----------       
    def test400_950_ShouldRaiseExceptionOnMissingFileNameCA03(self):
        'Fail on setting aries file with no name'
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing aries file")       
        
#----------           
    def test400_960_SholdRaiseExceptionOnMissingFileCA03(self):
        'Fail on setting aries file that does not exist'
        testFile = self.RANDOM_LOG_FILE+".txt"
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing aries file") 



#==================== Fix.setStarFile ===================              
# 500 setStarFile
#    Analysis
#        inputs:
#            starFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  string with absolute filepath                
#            also:    writes "Star file\tf.txt" to log file
#
#    Happy tests:
#        ariesFile:
#            test 010:    legitimate file, no parm name
#            test 020:    legitimate file, named parm  -> verify correct return value                          
#            test 030:    legitimate file name  -> verify correct log 
#    Sad tests:
#        ariesFile:
#            test 910:    nonstring file name
#            test 920:    missing file prefix
#            test 930:    missing .txt file extension
#            test 940:    missing .txt file extension, but presence of "txt" in name
#            test 950:    missing parm
#            test 960:    missing file
#
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
#---------- 
    def test500_010_ShouldSetstarFileWithOutKeywordParmCA03(self):
        'Set star file without keyword parm'
        testFile = self.mapFileToTest("validStarFile")
        theFix = F.Fix()
        try:
            result = theFix.setStarFile(testFile)
        except Exception as e:
            self.fail("Minor: " + str(e))
        self.assertNotEquals(-1, result.find(testFile), 
                             "Major:  setStarFile() is not returning file name")
        self.assertNotEquals(-1, result.find(os.path.abspath(testFile)), 
                             "Minor:  setStarFile() is not returning abspath of file name")

#----------
    def test500_020_ShouldConstructWithKeywordParmCA03(self):
        'Set star file with keyword parm'
        testFile = self.mapFileToTest("validStarFile")
        theFix = F.Fix()
        try:
            result = theFix.setStarFile(starFile = testFile)
        except Exception as e:
            self.fail("Minor: " + str(e))
        self.assertNotEquals(-1, result.find(testFile), 
                             "Major:  setStarFile() is not returning file name")
        self.assertNotEquals(-1, result.find(os.path.abspath(testFile)), 
                             "Minor:  setStarFile() is not returning abspath of file name")
 
#----------
    def test500_030_ShouldSetValidStarFileCA03(self):
        'Set star file and verify string is written to file'
        testFile = self.mapFileToTest("validStarFile")
        theFix = F.Fix()
        theFix.setStarFile(testFile)
        with open(self.DEFAULT_LOG_FILE, "r") as theLogFile:
            logFileContents = theLogFile.readlines()
            self.assertNotEquals(-1, logFileContents[-1].find(self.starFileString), 
                                 "Major:  correct star file string not being logged"),
            self.assertNotEquals(-1, logFileContents[-1].find(os.path.abspath(testFile)),
                                 "Minor:  correct star file name not being logged") 
 
#----------       
    def test500_910_ShouldRaiseExceptionOnNonStringFileNameCA03(self):
        'Fail on setting star file with non-string name'
        testFile = 42
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string star file name")  
   
#----------     
    def test500_920_ShouldRaiseExceptionOnFileLengthErrorCA03(self):
        'Fail on setting star file with missing file prefix'
        testFile = ".xml"
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 star file name") 
#----------      
    def test500_930_ShouldRaiseExceptionOnNonXmlFile1CA03(self):
        'Fail on setting star  file with no txt extension'
        testFile = "star."
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non txt star file extension")

#----------        
    def test500_940_ShouldRaiseExceptionOnNonXmlFile2CA03(self):
        'Fail on setting star  file with txt name but not txt extension'
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between star file name and extension") 
 
#----------       
    def test500_950_ShouldRaiseExceptionOnMissingFileNameCA03(self):
        'Fail on setting star file with no name'
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing star file")       
        
#----------           
    def test500_960_SholdRaiseExceptionOnMissingFileCA03(self):
        'Fail on setting star file that does not exist'
        testFile = self.RANDOM_LOG_FILE+".txt"
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(testFile)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for missing star file")
      




#----------
#==================== Fix.getSightings ===================         
# 300 getSightings
#    Analysis
#        inputs:
#            via parm:  none
#            via file:  xml description of sighting
#        outputs:
#            returns:    ("0d0.0", "0d0.0")
#|            via file:    writes body/tdate/ttime/tadjustedAltitude/tlongitude/tlatitude
#                        sorted by date, time, body
#        entry criterion:
#            setSightingsFile must be called first
#
#    Happy tests:
#        sighting file 
#            test 010:     file with valid sightings -> should return ("0d0.0", "0d0.0")
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
#            sighting file with invalid mandatory tag (one of each:  fix, body, date, time, observation)
#            sighting file with invalid tag value (one of each:  date, time, observation, height, temperature, pressure, horizon)
#    Sad tests:
#        sightingFile:
#            sighting file not previously set
#            star file not previously set
#            aries file not previously set
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
#---------- 
    def test300_010_ShouldIgnoreMixedIndentation(self):
        'parse sighting file that valid tags'
        testFile = self.mapFileToTest("genericValidStarSightingFile")
        expectedResult = ("0d0.0", "0d0.0")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.starFileName)
        theFix.setAriesFile(self.ariesFileName)
        result = theFix.getSightings()
        self.assertTupleEqual(expectedResult, result, 
                              "Minor:  incorrect return value from getSightings")
        
#---------- 
    def test300_020_ShouldIgnoreMixedIndentation(self):
        'parse sighting file that has mixed indentation'
        testFile = self.mapFileToTest("genericValidSightingFileWithMixedIndentation")
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)
        theFix.setStarFile(self.starFileName)
        try:
            theFix.getSightings()
            self.assertTrue(True)
        except:
            self.fail("Major: getSightings failed on valid file with mixed indentation")
            
#---------- 
    def test300_030_ShouldLogOneSighting(self):
        'log one valid adjusted altitude'
        testFile = self.mapFileToTest("validOneStarSighting")
        targetStringList = ["Aldebaran", "2017-03-01", "23:40:01"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
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
                                         "Major:  Log entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
#---------- 
    def test300_040_ShouldLogMultipleSightingsInTimeOrder(self): 
        'Log multiple stars that sorting'   
        testFile = self.mapFileToTest("validMultipleStarSighting") 
        targetStringList = [
            ["Sirius", "2017-03-01", "00:05:05"],
            ["Canopus", "2017-03-02", "23:40:01"]
            ]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "Major: failure to find " + targetStringList[0][0] +  " in log " + self.RANDOM_LOG_FILE)
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index][0] in logFileContents[entryIndex])):
                self.fail("Major: failure to find star in log " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True  

#---------- 
    def test300_050_ShouldLogMultipleSightingsWithSameDateTime(self): 
        'Log multiple stars that require sorting using body name'        
        testFile = self.mapFileToTest("validMultipleStarSightingSameDateTime") 
        targetStringList = [
            ["Acrux", "2017-03-01", "00:05:05"],
            ["Sirius", "2017-03-01", "00:05:05"],
            ["Canopus", "2017-03-02", "23:40:01"]
            ]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "Major: failure to find " + targetStringList[0][0] +  " in log " + self.RANDOM_LOG_FILE)
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index][0] in logFileContents[entryIndex])):
                self.fail("Major: failure to find star in log " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True   

#---------- 
    def test300_060_ShouldHandleNoSightings(self):
        'ensure empty fix is handled without logging anything'       
        testFile = self.mapFileToTest("validWithNoSightings")
        
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        endOfSightingFileIndex = self.indexInList(self.starSightingString, logFileContents)
        self.assertLess(-1,endOfSightingFileIndex,
                           "Major: log file does not contain 'end of sighting file' entry " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True   
        
#---------- 
    def test300_070_ShouldIgnoreExtraneousTags(self): 
        'log information from recognized tags, ignore extraneous tags'   
        testFile = self.mapFileToTest("validWithExtraneousTags")   
        targetStringList = [
            ["Sirius", "2017-03-01", "00:05:05"],
            ]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "Major: failure to find " + targetStringList[0][0] +  " in log " + self.RANDOM_LOG_FILE)
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index][0] in logFileContents[entryIndex])):
                self.fail("Major: failure to find star in log " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True    

#---------- 
    def test300_080_ShouldLogStarWithNaturalHorizon(self):
        'log adjusted altitude for natural horizon'
        testFile = self.mapFileToTest("validOneStarNaturalHorizon")   
        targetStringList = ["Hadar", "2017-03-01", "23:40:01", "29d55.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
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
                                         "Major:  Log entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  

#---------- 
    def test300_080_ShouldLogStarWithArtificialHorizon(self):
        'log adjusted altitude for artificial horizon'
        testFile = self.mapFileToTest("validOneStarArtificialHorizon")
        targetStringList = ["Hadar", "2017-03-01", "23:40:01", "29d59.9"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
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
                                         "Major:  Log entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
#----------         
    def test300_090_ShouldLogStarWithDefaultSightingValues(self):
        'log adjusted altitude for star using default values'
        testFile = self.mapFileToTest("validOneStarWithDefaultValues")

        targetStringList = ["Hadar", "2017-03-01", "23:40:01", "29d59.9"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
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
 
#-----------        
    def test300_091_ShouldLogErrorOnMissingMandatoryTag(self):
        'Verify that missing mandatory tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidWithMissingMandatoryTags")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for missing mandatory tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True  

#----------
    def test300_092_ShouldLogErrorOnInvalidBody(self):
        'Verify that invalid body tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidBodyTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Minor:  failure to log number of sighting error for invalid body tag " + self.RANDOM_LOG_FILE)
        self.deleteNamedLogFlag = True

#----------
    def test300_093_ShouldLogErrorOnInvalidDate(self):
        'Verify that invalid date tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidDateTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid date tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True

#----------
    def test300_094_ShouldLogErrorOnInvalidTime(self):
        'Verify that invalid time tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidTimeTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid time tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        
#----------
    def test300_095_ShouldLogErrorOnInvalidObservation(self):
        'Verify that invalid observation tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidObservationTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid observation tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        

#----------
    def test300_096_ShouldLogErrorOnInvalidHeight(self):
        'Verify that invalid height tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidHeightTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid height tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        

#----------
    def test300_097_ShouldLogErrorOnInvalidTemperature(self):
        'Verify that invalid temperature tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidTemperatureTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.starFileName)
        theFix.setAriesFile(self.ariesFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid temperature tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True
        

#----------
    def test300_098_ShouldLogErrorOnInvalidPressure(self):
        'Verify that invalid pressure tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidPressureTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid pressure tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True

#----------
    def test300_099_ShouldLogErrorOnInvalidHorizon(self):
        'Verify that invalid horizon tag was flagged as sighting error'
        targetString = "Sighting errors:\t1"
        testFile = self.mapFileToTest("invalidHorizonTag")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.starFileName)
        theFix.setAriesFile(self.ariesFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        self.assertNotEquals(-1, self.indexInList(targetString, logFileContents),
                          "Major:  failure to log number of sighting error for invalid horizon tag " + self.RANDOM_LOG_FILE) 
        self.deleteNamedLogFlag = True        
        
    def test300_100_ShouldLogStarLatLon(self):
        'log geographical position with no interpolation of observation'
        testFile = self.mapFileToTest("validLatLon")
        targetStringList = ["Sabik", None, None, None, "-15d44.4", "247d23.7"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
         
#-----------        
    def test300_110_ShouldLogStarLatLonWithInterpolation(self):
        'log geographical position'
        testFile = self.mapFileToTest("validLatLonInterpolated")
        targetStringList = ["Betelgeuse", None, None, None, "7d24.3", "75d54.3"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
        
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
        
#---------- 
    def test300_910_ShouldRaiseExceptionOnNotSettingSightingsFile(self):
        'Raise exception on failure to set sighting file'
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()") 
    
    def test300_920_ShouldRaiseExceptionOnNotSettingStarFile(self):
        'Raise exception on failure to set star file'
        expectedDiag = self.className + "getSightings:"
        testFile = self.mapFileToTest("validOneStarSighting")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setAriesFile(self.ariesFileName)   
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set star file before getSightings()")   

    def test300_930_ShouldRaiseExceptionOnNotSettingAriesFile(self):
        'Raise exception on failure to set aries file'
        expectedDiag = self.className + "getSightings:"
        testFile = self.mapFileToTest("validOneStarSighting")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix = F.Fix()
        theFix.setSightingFile(testFile)
        theFix.setStarFile(self.ariesFileName)   
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set aries file before getSightings()")     

#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
    
    def mapFileToTest(self, target):
        for item in self.testToFileMap:
            if(item[0] == target):
                return item[1]
        return None