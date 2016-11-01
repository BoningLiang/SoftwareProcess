
class Angle(object):
    
    def __init__(self):
        self.degrees = 0
    
    def setDegrees(self, degrees = 0.0):
        if isinstance(degrees, float) or isinstance(degrees, int):
            self.degrees = degrees % 360
            return float(self.degrees)
        else:
            raise ValueError("Angle.setDegrees: Value Error")
    
    def checkDegrees(self, degreeString):
        if(degreeString is None):
            return 0
        else:
            try:
                int(degreeString)
            except ValueError:
                return 0
            return 1
    
    def checkMinutes(self, MinuteString):
        if(MinuteString is None):
            return 0
        else:
            try:
                floatMinute = float(MinuteString)
            except ValueError:
                return 0
            if(floatMinute<0):
                return 0
            else:
                if(self.checkMinutesIfOnlyHaveOneDecimalPlace(MinuteString) == 1):
                    return 1
                else:
                    return 0
            
    def checkMinutesIfOnlyHaveOneDecimalPlace(self, minutePortion):
        minutePortions = minutePortion.split(".")
        if(len(minutePortions) == 1):
            return 1
        else:
            if int(minutePortions[1])>9:
                return 0
            else:
                return 1
#             minutePoints = minutePortions[1].split()
#             if(len(minutePoints)!=1):
#                 return 0
#             else:
#                 return 1
    
    def setDegreesAndMinutes(self, angleString):
        if(angleString is None or angleString is ""):
            raise ValueError('Angle.setDegreesAndMinutes:')
        else:
            if(isinstance(angleString, basestring)):
                portions = angleString.split('d')
                if len(portions) is not 2:
                    raise ValueError('Angle.setDegreesAndMinutes:')
                else:
                    if(self.checkDegrees(portions[0]) == 1):
                        if(self.checkMinutes(portions[1]) == 1):
                            self.interpretDegreesAndMinutes(int(portions[0]), float(portions[1]))
                            return self.degrees
                        else:
                            raise ValueError('Angle.setDegreesAndMinutes:')
                    else:
                        raise ValueError('Angle.setDegreesAndMinutes:')
            else:
                raise ValueError('Angle.setDegreesAndMinutes:')
                
    def interpretDegreesAndMinutes(self, angleDegree, angleMinute):
        if angleDegree<0:
            angleDegree = -angleDegree
            self.degrees = 360.0 - (angleDegree+angleMinute/60.0)
        elif angleDegree>=0:
            self.degrees = angleDegree + angleMinute/60.0
        self.setDegrees(self.degrees)
    
    def add(self, angle = 0):
        if(isinstance(angle, Angle)):
            self.degrees = self.degrees + angle.degrees
            self.setDegrees(self.degrees)
            return float(self.degrees)
        else:
            raise ValueError('Angle.add:')
    
    def subtract(self, angle = 0):
        if isinstance(angle, Angle):
            self.degrees = self.degrees - angle.degrees
            self.setDegrees(self.degrees)
            return self.degrees
        else:
            raise ValueError('Angle.subtract: ')
    
    def compare(self, angle = 0):
        if(isinstance(angle, Angle)):
            if(self.degrees < angle.degrees ):
                return -1
            if(self.degrees > angle.degrees ):
                return 1
            if(self.degrees == angle.degrees ):
                return 0
        else:
            raise ValueError('Angle.compare: miss or wrong parameter angle')

    def getString(self):
        angleDegreeInt = int(self.degrees)
        angleMinuteFloat = self.degrees-angleDegreeInt
        angleMinute=round(angleMinuteFloat * 60, 1)
        angleDegreeString = str(angleDegreeInt) + "d" + str(angleMinute)
        return angleDegreeString
        
    def getDegrees(self):
        return float(self.degrees)