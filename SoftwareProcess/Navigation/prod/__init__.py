import Fix
import Angle
   
theFix = Fix.Fix()
sightingFilePath = theFix.setSightingFile("sightingFileCA05.xml")
starFilePath = theFix.setStarFile("stars.txt")
ariesFilePath = theFix.setAriesFile("aries.txt")
assumedLatitude = "N27d59.5"
assumedLongitude = "85d33.4"
approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)
print "("+str(approximatePosition[0])+", "+str(approximatePosition[1])+")"
# 
# 
# theFix = Fix.Fix()
# sightingFilePath = theFix.setSightingFile("sightingFile2.xml")
# starFilePath = theFix.setStarFile("stars.txt")
# ariesFilePath = theFix.setAriesFile("aries.txt")
# assumedLatitude = "S53d38.4"
# assumedLongitude = "74d35.3"
# approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)
# print "("+str(approximatePosition[0])+", "+str(approximatePosition[1])+")"
# 
# 


