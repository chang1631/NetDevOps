#!/usr/bin/env python3.11
from matplotlib import pyplot as plt
from pathlib import Path
from netmiko import Netmiko
import os, re

# 当前目录的路径
current_dir = Path(__file__).parent

def mat_pie(lb_list, count_list, pie_title):
    """
    绘制netflow应用流量饼状图

    参数：
        lb_list(list): 标签列表
        count_list(list): 流量信息列表
        pie_title(str): 饼状图的标题
    """
    plt.figure(figsize=(6,6))

    patches, lb_text, pie_text = plt.pie(count_list,
                                        labels=lb_list, # 每个扇区显示对应的 label 
                                        labeldistance=1.1,
                                        autopct='%3.1f%%',
                                        shadow=False,
                                        startangle=90,
                                        pctdistance=0.6)
    for txt in lb_text:
        txt.set_size = 30
    for txt in pie_text:
        txt.set_size = 30
    plt.axis('equal')
    plt.title(pie_title)

    # 将标签标识置于左下角
    plt.legend(patches, lb_list, loc='lower left')

    # 在当前目录中存储PNG格式的饼状图
    plt.savefig(f'{current_dir}{os.sep}result.png')
    plt.show()

def netmiko_get_netflow_cache(host,
                              username='admin',
                               password='Cisc0123',
                               cmd='show flow monitor name qytang-monitor cache format table',
                               device_type='cisco_ios',
                               ssh_port=22):
    """
    获取网络设备的netflow统计信息

    参数：
        host(str): 网络设备的IP地址
        username(str): 用户名
        password(str): 密码
        cmd(str): 命令
        device_type(str): 设备类型
        ssh_port(int): SSH端口号
    返回：
        元组：包含标签列表和流量信息列表
    """
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'port':ssh_port
    }

    try:
        net_connect = Netmiko(**device_info)
        result = net_connect.send_command(cmd)
        # 打印设备返回的netflow统计信息
        print(result)
        # 用正则表达式匹配并获取SSH、Telnet和Ping占用流量的相关结果(元组)
        port_ssh = re.findall(r'(port ssh)\s+(\d+)', result)[0]
        port_telnet = re.findall(r'(port telnet)\s+(\d+)', result)[0]
        layer7_ping = re.findall(r'(layer7 ping)\s+(\d+)', result)[0]
        # 将获取到的结果存入一个列表
        all_netflow_data = [port_ssh,port_telnet,layer7_ping]
        # 将列表中的元组按名称和流量信息进行拆分
        # lb是标签元组，count是流量信息元组
        lb, count = list(zip(*all_netflow_data))
        # 将拆分后的元组转换成列表
        lb_list =list(lb)
        count_list = [int(x) for x in count]

        net_connect.disconnect()
        return lb_list, count_list
    except Exception as e:
        print(f'SSH连接失败: {host} error: {str(e)}')

if __name__ == '__main__':
    netflow_data = netmiko_get_netflow_cache('10.10.1.101')
    lb_list = netflow_data[0]
    count_list = netflow_data[1]
    mat_pie(lb_list,count_list, '第三天作业Netflow')