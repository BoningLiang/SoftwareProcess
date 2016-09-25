import Navigation.prod.Angle as Angle

# ---------- constructor ----------
# Instantiate angles

angle1 = Angle.Angle()
angle2 = Angle.Angle()
angle3 = Angle.Angle()
angle4 = Angle.Angle()


# ---------- set ----------
angle1Degrees = angle1.setDegreesAndMinutes("45d0.0")   #angle1Degrees should be 45.0
angle2Degrees = angle2.setDegrees(-19.5)        #angle2Degrees should be 340.5
angle3Degrees = angle3.setDegreesAndMinutes("0d30.0")   #angle3Degrees should be 0.5


# Attempts to set an invalid value should result
# in a ValueError exception bearing a diagnostic message
try:
    invalidAngle = angle2.setDegrees("")
except ValueError as raisedException:
    diagnosticString = raisedException.args[0]


# ---------- add ----------
# Add angle2 to angle1; save result in angle1; return result as degrees
# 45d0 + 340d30 = 385d30 = 25d30 = 25.5 degrees
addedDegrees1 = angle1.add(angle2)  #addedDegress1 should be 45d0 + 340d30 = 385d30 = 25d30 = 25.5 
# Add angle3 to angle2; save result in angle2; return result as degrees
addedDegrees3 = angle2.add(angle3)  #addedDegrees should be 340d30 + 0d30 = 340d60 = 341d0 = 341.0

# Attempts to pass a parm that is not an instance of Angle
# should result in a ValueError exception bearing a diagnostic message.
try:
    angle1.add("42d0")
except ValueError as raisedException:
    diagnosticString = raisedException.args[0]


# ---------- subtract ----------
# Subtract angle1 from angle4; save result in angle4; return result as degrees
subtractedDegrees = angle4.subtract(angle1) #subtracted degrees should be 0d0 - 25d30 = -25d30 = 334d30= 334.5

# Attempts to pass a parm that is not an instance of Angle
# should result in a ValueError exception bearing a diagnostic message.
try:
    angle1.add(0)
except ValueError as raisedException:
    diagnosticString = raisedException.args[0]



# ---------- compare ----------
# Compare angle2 to angle1.  Return -1 if angle1 is less than angle2,
# +1 if angle1 is greater than angle2
# 0 if angle1 is equal to angle2
angle1.setDegrees(45.0)
angle2.setDegrees(45.1)
result = angle1.compare(angle2) #result should be -1


# Attempts to pass a parm that is not an instance of Angle
# should result in a ValueError exception bearing a diagnostic message
try:
    angle1.compare(42.0)
except ValueError as raisedException:
    diagnosticString = raisedException.args[0]




# ---------- getString ----------
angle1String = angle1.getString()   #angle1String should be "45d0.0"
angle2String = angle2.getString()   #angle2String should be "45d6.0"
angle3.setDegrees(45.123)
angle3String = angle3.getString()   #angle3String should be "45d7.4"



# ---------- getDegrees ----------
angle1Degrees = angle1.getDegrees()   #angle1String should be 45.0
angle2Degress = angle2.getDegrees()   #angle2String should be 45.1
angle3Degrees = angle3.getDegrees()   #angle3String should be 45.1
