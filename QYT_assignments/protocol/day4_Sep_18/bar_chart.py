#!/usr/bin/env python3.11
from matplotlib import pyplot as plt
from pathlib import Path
import os

# 图片存储路径
save_dir = f'{Path(__file__).parent}{os.sep}graph'

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

def mat_bar(name_list, count_list, title, x_label, y_label, color_list):
    plt.figure(figsize=(6, 6))

    plt.bar(name_list, count_list, width=0.5, color=color_list)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.savefig(f'{save_dir}{os.sep}result1.png')
    plt.show()

if __name__ == '__main__':
    name_list = ['8月', '9月', '10月', '11月']
    count_list = [123, 555, 354, 888]
    bar_name = '2025销售状况'
    x_label = '月份'
    y_label = '万'
    colors = ['red', 'blue', 'green', 'yellow']
    mat_bar(name_list, count_list, bar_name, x_label, y_label, colors)