# from datetime import datetime,timedelta, strftime
from datetime import *

cur_datetime=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print(cur_datetime)

fiveDaysago = datetime.now() - timedelta(days=5)
print("%s"%fiveDaysago,file=open('save_fivedayago_time_'+cur_datetime+'.txt','w'))