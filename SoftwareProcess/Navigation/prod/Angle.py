class Angle(object):
    
    def __init__(self):
        self.degrees = 0
    
    def setDegrees(self,degrees):
        if(isinstance(degrees, float)):
            self.degrees = degrees % 360
            return self.degrees
        else:
            raise ValueError("Value Error")
    
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
            minutePoints = minutePortions[1].split()
            if(len(minutePoints)!=1):
                return 0
            else:
                return 1
    
    def setDegreesAndMinutes(self, angleString):
        if(angleString is None):
            raise ValueError('Value Error')
        else:
            if(isinstance(angleString, basestring)):
                portions = angleString.split('d')
                if(len(portions)!=2):
                    raise ValueError('Value Error')
                else:
                    if(self.checkDegrees(portions[0]) == 1):
                        if(self.checkMinutes(portions[1]) == 1):
                            self.interpretDegreesAndMinutes(int(portions[0]), float(portions[1]))
                            return self.degrees
                        else:
                            raise ValueError('Value Error')
                    else:
                        raise ValueError('Value Error')
            else:
                raise ValueError('Value Error')
                
    def interpretDegreesAndMinutes(self, angleDegree, angleMinute):
        self.degrees = angleDegree + angleMinute/60
        self.setDegrees(self.degrees)
    
    def add(self, angle):
        if(isinstance(angle, Angle)):
            self.degrees = self.degrees + angle.degrees
            self.setDegrees(self.degrees)
            return self.degrees
        else:
            raise ValueError('Value Error')
    
    def subtract(self, angle):
        self.degrees = self.degrees - angle.degrees
        self.setDegrees(self.degrees)
        return self.degrees
    
    def compare(self, angle):
        if(isinstance(angle, Angle)):
            if(self.degrees < angle.degrees ):
                return -1
            if(self.degrees > angle.degrees ):
                return 1
            if(self.degrees == angle.degrees ):
                return 0
        else:
            raise ValueError('Value Error')

    def getString(self):
        angleDegreeInt = int(self.degrees)
        angleMinuteFloat = self.degrees-angleDegreeInt
        angleMinute=round(angleMinuteFloat * 60, 1)
        angleDegreeString = str(angleDegreeInt) + "d" + str(angleMinute)
        return angleDegreeString
        
    def getDegrees(self):
        return self.degrees