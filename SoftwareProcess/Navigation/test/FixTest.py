import unittest
import Navigation.prod.Fix as F

class FixTest(unittest.TestCase):



    def setUp(self):
        pass

    def tearDown(self):
        pass

# -----------------------------------------------------------------------
# ---- Acceptance Tests
# 100 constructor
#
#
# Happy path 

    def test100_010_ShouldConstruct(self):
        self.assertIsInstance(F.Fix(), F.Fix)
        self.assertIsInstance(F.Fix('hello.log'), F.Fix)
        
        
# 200 setSightingFile
#
#
#
# Happy path

    