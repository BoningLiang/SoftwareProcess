import re

timeStr = "^(?P<hour>[0-2]?[0-3]):(?P<minute>[0-5]?[0-9]):(?P<second>[0-5]?[0-9])$"
#date = "^(?P<month>[0-3]?[0-9])/(?P<day>[0-3]?[0-9])/(?P<year>[0-9]{4})$"
dateStr = "^(?P<year>[0-9]{4})\-(?P<month>[0-3]?[0-9])\-(?P<day>[0-3]?[0-9])$"

date1 = "2009-12-12"
match = re.search(dateStr, date1)
 
if match:
    print "match"


time1 = "11:00:00"
time2 = "23:59:59"
time3 = "24:59:59"
  
match1 = re.search(timeStr, time1)
match2 = re.search(timeStr, time2)
match3 = re.search(timeStr, time3)
  
if match1:
    print "match1"
      
if match2:
    print "match2"
      
if match3:
    print "match3"