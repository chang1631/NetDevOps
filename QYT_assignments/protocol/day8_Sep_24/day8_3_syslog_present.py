#!/usr/bin/env python3
from matplotlib import pyplot as plt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from pathlib import Path
from typing import List, Any
import os,sys

# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前文件所在的父目录路径
parrent_dir = working_dir.parent
# 获取当项目根路径
project_root = parrent_dir.parent
sys.path.insert(1, str(project_root))

from day8_Sep_24.day8_1_syslog_create_table import engine, db_file_name, Syslog

def query_grouped_fields(session, model, group_field, *fields) -> List[List[Any]]:
    """
    通用查询函数
    
    参数：
        session: SQLAlchemy session
        model: ORM 表模型
        group_field: 分组字段
        fields: 需要查询的字段（可变参数）
    返回: 
        [list1, list2, ...] 每个字段对应一个列表
    """
    # 构建查询，自动加上 func.count()
    query = session.query(func.count(group_field), *fields).group_by(group_field)

    # 执行查询
    results = query.all()

    # 每个字段一个列表（第 0 列是 count）
    output_lists = [[] for _ in range(len(fields) + 1)]
    for row in results:
        for idx, value in enumerate(row):
            output_lists[idx].append(value)

    return output_lists



def syslog_pie_gen(label_list, count_list, pie_title, filename, other_list=[]):
    """
    绘制饼状图

    参数：
        label_list(list): 标签列表
        count_list(list): 数据列表
        pie_title(str): 饼状图标题
        filename(str): 保存的饼状图文件名
        other_list(list): 额外的列表
    返回：
        列表：包含被整合后的数据
    """
    plt.figure(figsize=(6,6))

    patches, l_text, p_text = plt.pie(count_list,
                                      labels=label_list,
                                      labeldistance=1.1,
                                      autopct='%3.1f%%',
                                      shadow=False,
                                      startangle=90,
                                      pctdistance=0.6)
    for t in l_text:
        t.set_size = 30
    for t in p_text:
        t.set_size = 30
    
    plt.axis('equal')
    plt.title(pie_title)
    plt.legend()

    images_dir = os.path.join(os.path.dirname(working_dir), 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    image_path = os.path.join(images_dir, filename)
    plt.savefig(image_path)
    print(f"图片已保存到: {image_path}")
    plt.show()

    # 将label_list和count_list中的数据根据对应index进行打包并返回
    # 如果other_list为空，则返回二元元组
    if other_list:
        return sorted(zip(label_list, other_list, [int(count) for count in count_list]))
    # 如果other_list为空，则返回三元元组
    else:
        return sorted(zip(label_list, [int(count) for count in count_list]))


if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    # 绘制SYSLOG严重级别分布饼状图
    level_count_list, level_list = query_grouped_fields(session, Syslog, Syslog.severity_level_name, Syslog.severity_level_name)
    print(level_list)
    print(level_count_list)
    res1=syslog_pie_gen(level_list, level_count_list, 'SYSLOG严重级别分布图', 'syslog_severity_pie.png')

    # 绘制SYSLOG设备分布饼状图
    device_count_list, device_list, ip_list = query_grouped_fields(session, Syslog, Syslog.device_name, Syslog.device_name, Syslog.device_ip)
    print(device_list)
    print(ip_list)
    print(device_count_list)
    res2=syslog_pie_gen(device_list, device_count_list, 'SYSLOG设备分布图', 'syslog_device_pie.png',ip_list)