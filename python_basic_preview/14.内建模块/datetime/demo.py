import datetime

# now = datetime.datetime.now()
# print(now)
#
# otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
# print(otherStyleTime)
#
# otherStyleTime = now.strftime("%Y-%m-%d")
# print(otherStyleTime)
#
# otherStyleTime = now.strftime("%I:%M:%S %p")
# print(otherStyleTime)
#
# otherStyleTime = now.strftime("今天是今天的第%j天")
# print(otherStyleTime)
#
# otherStyleTime = now.strftime("%%")
# print(otherStyleTime)
#
# threeDaysAgo = (datetime.datetime.now() - datetime.timedelta(days=3))
# print(threeDaysAgo)
#
today = datetime.date.today()
print(today)

tenDaysBefore = today - datetime.timedelta(days = 10)
print(tenDaysBefore)
#
# tenDaysAfter = today + datetime.timedelta(days = 10)
# print(tenDaysAfter)

i = datetime.datetime.now()
print("当前的日期和时间是%s"%i)

print("当前的年份是%s"%i.year)

print("当前的月份是%s"%i.month)

print("当前的日期是%s"%i.day)

print("当前的小时是%s"%i.hour)

print("当前的分钟是%s"%i.minute)

print("当前的秒是%s"%i.second)
