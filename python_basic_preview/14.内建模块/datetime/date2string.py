from dateutil import parser
from datetime import datetime, timedelta, timezone
import sys


# date_string = '2023-03-31 12:30:45'
# date_format = '%Y-%m-%d %H:%M:%S'
#
# date_obj = datetime.strptime(date_string,date_format)
# print(date_obj - timedelta(days=3))
# print(sys.path)

# strtime = str(datetime.now())
# print(strtime)
# print(type(strtime))
#
# i= parser.parse(strtime)
# print(i + timedelta(days=5))
#
# p=datetime(2018,5,1,15,23,38,731)
# print(type(p))

tzutc_8 =  timezone(timedelta(hours=8))
tzutc_1 =  timezone(timedelta(hours=1))
print(datetime.now())
print(datetime.now().astimezone(tzutc_1))
