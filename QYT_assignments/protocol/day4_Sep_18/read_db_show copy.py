#!/usr/bin/env python3.11
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from datetime import datetime, timedelta
import sys, os
from matplotlib import pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as mtick


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

# 图片存储路径
save_dir = f'{Path(__file__).parent}{os.sep}graph'

# 将当前路径追加至Python编译器的path中
current_dir = Path(__file__).parent
sys.path.insert(1, str(current_dir))

from day4_1_create_db import RouterMonitor, db_file_name

# 创建数据库会话
engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()


def mat_line(lines_list, title, x_label, y_label, filename):
    """
    绘制线型图
    """
    fig = plt.figure(figsize=(6, 6))

    ax = fig.add_subplot(111)

    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))
    # 设置主刻度间隔为 10 分钟
    ax.xaxis.set_major_locator(mdate.MinuteLocator(interval=10))

    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%3.1f%%'))
    ax.set_ylim(ymin=0, ymax=100)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    fig.autofmt_xdate()
    
    for x_list, y_list, line_style, color, line_name in lines_list:
        ax.plot(x_list, y_list, linestyle=line_style, color=color, label=line_name)

    ax.legend(loc='upper left')

    plt.savefig(filename)
    plt.show()


def show_cpu_mem_usage():
    """
    从数据库中获取最近1小时内的数据并绘制CPU利用率和内存利用率的线型图

    返回:
        CPU利用率和内存利用率的线型图的文件路径
    """
    # 最近一个小时
    last_one_hour = datetime.now() - timedelta(hours=1) 

    color_list = ['red','blue', 'green', 'yellow']
    line_style_list = ['solid', 'dashed']

    # 先从表中筛选出唯一的device_ip
    unique_device_ips = session.query(RouterMonitor.device_ip).distinct().all()
    # [('10.10.1.101',), ('10.10.1.102',)]
    # 提取列表unique_device_ips中每个元组的值到一个新的列表
    device_list = [ip[0] for ip in unique_device_ips]

    # 定义CPU和MEM的空列表用于后续存放每台设备数据列表和制图参数
    lines_list_cpu=[]
    lines_list_mem=[]
    # 初始化line的颜色ID
    color_id = 0
    
    # 基于每台设备的IP筛选出最近一小时内的记录
    for ip in device_list:
        records = (
            session.query(RouterMonitor).filter(RouterMonitor.device_ip == ip, 
                                                RouterMonitor.record_datetime >= last_one_hour
                                                )
                                                .order_by(RouterMonitor.record_datetime).all()
        )
        # 提取x轴的时间数据和y轴的利用率数据并添加至对应的列表
        line_x_list = [r.record_datetime for r in records]
        line_y_list_cpu = [r.cpu_usage_percent for r in records]
        # 计算出内存的利用率并添加至对应的列表
        line_y_list_mem = []
        for r in records:
            mem_use = r.mem_use
            mem_free = r.mem_free
            mem_usage = (mem_use/(mem_use + mem_free)) * 100
            line_y_list_mem.append(mem_usage)
        # 将CPU利用率相关的数据和制图参数追加至列表lines_list_cpu
        lines_list_cpu.append([
            line_x_list,
            line_y_list_cpu,
            line_style_list[0],
            color_list[color_id],
            ip
        ])
        # 将内存利用率相关的数据和制图参数追加至列表lines_list_mem
        lines_list_mem.append([
            line_x_list,
            line_y_list_mem,
            line_style_list[1],
            color_list[color_id],
            ip
        ])
        color_id += 1
    # 定义PNG图片的存储路径及文件名
    cpu_usage_filename = f'{save_dir}{os.sep}cpu_usage1.png'
    mem_usage_filename = f'{save_dir}{os.sep}mem_usage1.png'
    mat_line(lines_list_cpu, 'CPU利用率', '记录时间','百分比', cpu_usage_filename)
    mat_line(lines_list_mem, 'MEM利用率', '记录时间','百分比', mem_usage_filename)

    print(f'CPU利用率和内存利用率的线型图绘制完成，文件路径为：\n{cpu_usage_filename}\n{mem_usage_filename }')
    return cpu_usage_filename, mem_usage_filename


if __name__ == '__main__':
    show_cpu_mem_usage()