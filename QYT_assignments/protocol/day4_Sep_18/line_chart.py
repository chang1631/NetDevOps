#!/usr/bin/env python3.11
from matplotlib import pyplot as plt
from pathlib import Path
import os

# 图片存储路径
save_dir = f'{Path(__file__).parent}{os.sep}graph'

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

def mat_line(lines_list, title, x_label, y_label):
    fig = plt.figure(figsize=(6, 6))

    ax = fig.add_subplot(111)

    import matplotlib.dates as mdate
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))

    import matplotlib.ticker as mtick
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%3.1f%%'))

    ax.set_ylim(ymin=0, ymax=100)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    fig.autofmt_xdate()
    
    for x_list, y_list, line_style, color, line_name in lines_list:
        ax.plot(x_list, y_list, linestyle=line_style, color=color, label=line_name)

    ax.legend(loc='upper left')

    plt.savefig(f'{save_dir}{os.sep}result2.png')

    plt.show()
    
if __name__ == '__main__':
    from datetime import datetime, timedelta
    from random import random, choice

    line_no = 2

    data_points_count = 10

    color_list = ['red','blue', 'green', 'yellow']

    line_style_list = ['solid', 'dashed']

    now = datetime.now()

    lines_list = []

    for l in range(line_no):
        line_name = f'line{l+1}'
        line_x_list = []
        line_y_list = []
        for d in range(data_points_count):
            line_x_list.append(now + timedelta(minutes=d))
            line_y_list.append(random()*100)
        
        lines_list.append([line_x_list, line_y_list, choice(line_style_list), choice(color_list), line_name])
    
    mat_line(lines_list, 'CPU利用率', '时间', '%')