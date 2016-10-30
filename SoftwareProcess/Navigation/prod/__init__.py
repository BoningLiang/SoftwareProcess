
import Fix
  
theFix = Fix.Fix()

theFix.setSightingFile("sightingFile.xml")

starFilePath = theFix.setStarFile("stars.txt")

ariesFilePath = theFix.setAriesFile("aries.txt")

approximatePosition = theFix.getSightings()