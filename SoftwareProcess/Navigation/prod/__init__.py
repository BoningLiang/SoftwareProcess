
# n = 'ttt'
# try:
#     float(n)
# except:
#     isFloat = False
# else:
#     isFloat = True
#     
# print isFloat



# h=unicode("5.5")
# print type(h)

# try:
#     h="6.0"
#     h=float(h)
# except:
#     print "ttt"


# test1 = "xml"
# test2 = "hello.xml"
# print ".xml" not in test1
# print ".xml" not in test2

# test1 = '.xml'
# t = test1.split(".")
# print t[0]
# print t[1]
# print t[0] == ""

import Fix as F
 
testFile = "CA02_300_ValidMultipleStarSighting.xml"
theFix = F.Fix()
theFix.setSightingFile(testFile)
theFix.getSightings()


# testFile = "CA02_300_ValidWithMixedIndentation.xml"
# theFix = F.Fix()
# theFix.setSightingFile(testFile)
# theFix.setStarFile("stars.txt")
# theFix.setAriesFile("aries.txt")
# theFix.getSightings()
# try:
#     theFix.getSightings()
# except:
#     print("Major: getSightings failed on valid file with mixed indentation")  

# test1 = "a"
# test2 = "b"
# test3 = "c"
# test4 = "d"
# print not (test1 == "b" or test1 == "a")

# import Angle
#  
# theAngle1 = Angle.Angle()
# theAngle2 = Angle.Angle()
# theAngle3 = Angle.Angle()
# 
# p = -10.44/60.0
# 
# theAngle1.setDegrees(-10.44/60.0)
# theAngle2.setDegrees(p)
# theAngle3.setDegrees(-0.174)
# 
# print theAngle1.getDegrees()
# print theAngle2.getDegrees()
# print theAngle3.getDegrees()