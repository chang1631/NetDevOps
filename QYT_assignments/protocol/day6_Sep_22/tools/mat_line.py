#!/usr/bin/env python3.11
from matplotlib import pyplot as plt
from pathlib import Path
import os

# 图片存储路径
save_dir = f'{Path(__file__).parent.parent}{os.sep}graph'

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

def mat_line(lines_list, title, x_label, y_label, filename):
    fig = plt.figure(figsize=(6, 6))

    ax = fig.add_subplot(111)

    import matplotlib.dates as mdate
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))

    import matplotlib.ticker as mtick
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))    # y轴的数据会被替换成接口的速率值

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    fig.autofmt_xdate()
    
    for x_list, y_list, line_style, color, line_name in lines_list:
        ax.plot(x_list, y_list, linestyle=line_style, color=color, label=line_name)

    ax.legend(loc='upper left')

    plt.savefig(f'{save_dir}{os.sep}{filename}')

    plt.show()
    
