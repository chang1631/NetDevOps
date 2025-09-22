#!/usr/bin/env python3.11
from sqlalchemy.orm import sessionmaker
from day6_1_create_db import InterfaceMonitor, engine
from pathlib import Path
import sys, os
import numpy as np
from pprint import pprint

parent_dir = Path(__file__).parent
sys.path.insert(1,str(parent_dir))

from tools.mat_line import mat_line

from datetime import datetime, timedelta

Session = sessionmaker(bind=engine)
session = Session()

# 计算出最近的一小时
now = datetime.now()
last_one_hour = now - timedelta(hours=8)

# 供随机选择的线条颜色
color_list = ['orange', 'gold', 'violet', 'red', 'brown', 'pink', 'gray', 'lime']
# 供随机选择的线条的类型
line_style_list = ['solid', 'dashed','dashdot', 'dotted']

# 筛选出唯一device_ip和interface_name的组合
router_if_infos = session.query(InterfaceMonitor.device_ip,
                                InterfaceMonitor.interface_name).group_by(InterfaceMonitor.device_ip,
                                                                          InterfaceMonitor.interface_name).all()
"""
# 获取到的router_if_infos是一个列表，如下所示:
 [
    ('10.10.1.101', 'GigabitEthernet1')
    ('10.10.1.101', 'GigabitEthernet2')
    ('10.10.1.101', 'GigabitEthernet3')
    ('10.10.1.101', 'Null0')
    ('10.10.1.102', 'GigabitEthernet1')
    ('10.10.1.102', 'GigabitEthernet2')
    ('10.10.1.102', 'GigabitEthernet3')
    ('10.10.1.102', 'Null0')
 ]
"""


# 接口入方向速率及线形参数列表
in_speed_lines_list =[]
# 接口出方向速率及线形参数列表
out_speed_lines_list =[]

count = 0

for device_ip, interface_name in router_if_infos:
    # 根据设备IP和接口的名称筛选出对应接口最近一小时内的所有记录
    # 每一次循环就是一台设备的一个接口
    # 将返回的<class 'sqlalchemy.orm.query.Query'>的实例赋值给device_if_info
    device_if_info = session.query(InterfaceMonitor).\
        filter(InterfaceMonitor.device_ip == device_ip,
               InterfaceMonitor.interface_name == interface_name).\
        filter(InterfaceMonitor.record_datetime >= last_one_hour)
    
    # 保存入向字节的列表
    in_bytes_list = []
    # 保存出向字节的列表
    out_bytes_list = []
    # 保存记录时间的列表
    record_time_list = []

    # 遍历该接口的记录条目，提取入方向、出方向的数据和记录时间并添加至对应的列表
    for device_if in device_if_info:
        in_bytes_list.append(device_if.in_bytes)
        out_bytes_list.append(device_if.out_bytes)
        record_time_list.append(device_if.record_datetime)
    

    # # ------------使用Numpy计算字节的增量------------
    diff_in_bytes_list = list(np.diff(in_bytes_list))
    diff_out_bytes_list = list(np.diff(out_bytes_list))

    # # ------------使用Numpy计算时间的增量(秒)------------
    diff_record_time_list = [x.seconds for x in np.diff(record_time_list)]

    # # ------------计算入向和出向的速率------------
    in_speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2),
                         zip(diff_in_bytes_list, diff_record_time_list)))

    out_speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2),
                         zip(diff_out_bytes_list, diff_record_time_list)))

    # # 切掉第一个时间记录点，剩下为速率的记录时间
    record_time_list = record_time_list[1:]

    # # 开始数据清洗
    clean_record_time_list = []
    clean_in_speed_list = []
    clean_out_speed_list = []

    # 将记录时间、入方向速率和出方向速率对应的元素进行打包
    # 遍历打包后的元素，并将入方向和出方向流量都大于0的元组中的数据添加至对应的最终列表中
    for r, i, o in zip(record_time_list, in_speed_list, out_speed_list):
        if i > 0 and o > 0:
            clean_record_time_list.append(r)
            clean_in_speed_list.append(i)
            clean_out_speed_list.append(o)

    
    # 判断如果该接口的clean_in_speed_list和clean_out_speed_list列表都有数据就添加到lines_list列表
    # 若该接口没有流量则不会被绘制
    if len(clean_in_speed_list) > 0 and len(clean_out_speed_list) > 0:
        print(device_if.interface_name)
        in_speed_lines_list.append([clean_record_time_list,
                                    clean_in_speed_list,
                                    line_style_list[count % len(line_style_list)],  # count % len(line_style_list) 使用余数可以确保count不会超出列表的长度范围
                                    color_list[count % len(color_list)],    
                                    f'RX:{device_ip}:{interface_name}'])
        out_speed_lines_list.append([clean_record_time_list,
                                    clean_out_speed_list,
                                    line_style_list[count % len(line_style_list)],
                                    color_list[count % len(color_list)],
                                    f'TX:{device_ip}:{interface_name}'])
    # 该接口的数据已经采集完成，计数器叠加一，进入下一个接口的数量收集及清洗
    count += 1

# 绘制该线形图
mat_line(in_speed_lines_list, '入向速率','记录时间','kbps','in_speed.png')
mat_line(out_speed_lines_list, '出向速率','记录时间','kbps','out_speed.png')