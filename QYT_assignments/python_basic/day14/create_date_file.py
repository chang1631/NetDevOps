from datetime import datetime, timedelta
from locale import D_FMT
from pathlib import Path
import os

# 获取当前python文件的路径
current_path = Path(__file__).resolve()
# 获取当前路径的父目录
parent_path = current_path.parent
# 获取当前的时间
time_now = datetime.now()
# 获取五天前的时间
time_five_days_ago = time_now - timedelta(days=5)
# 转换当前时间的显示格式将其作为文件名的末尾
filename_time = time_now.strftime(f'%Y-%m-%d_%H-%M-%S')
# 按要求创建以当前日期命名的txt文件并写入五天前的时间
datefile = open(f'{parent_path}{os.sep}save_fivedayago_time_{filename_time}.txt', 'w')
datefile.write(str(time_five_days_ago))