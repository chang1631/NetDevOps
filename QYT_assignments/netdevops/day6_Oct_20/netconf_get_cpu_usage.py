#!/usr/bin/env python3
from pathlib import Path
from jinja2 import Template
import os,sys
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent

# jinja2模板路径
xml_path = f'{parrent_dir}{os.sep}rpc_jinja2{os.sep}'

from netconf_client import netconfig_request
from device_credentials import netconf_devices
import xmltodict

def monitor_cpu(device_ip, username, password, monitor_type='5s'):
    """
    通过NETCONF RPC获取指定时间间隔内的设备CPU利用率

    参数：
        ip(str): 设备的管理IPv4地址
        username(str): 用户名
        password(str): 密码
        monitor_type(str): 时间间隔
    返回：
        字符串格式的CPU利用率
    """
    # 根据monitor_type定义time_interval的值
    if monitor_type == '1m':
        time_interval = 'one-minute'
    elif monitor_type == '5m':
        time_interval = 'five-minutes'
    else:
        time_interval = 'five-seconds'
    # 打开cpu_monitor模板并进行渲染
    with open(xml_path + 'cpu_monitor.jinja2', encoding='utf-8') as f:
        netconf_template = Template(f.read())
    netconf_payload_xml = netconf_template.render(time_interval=time_interval)
    # 发送获取CPU利用率的NETCONF RPC请求
    result_xml = netconfig_request(device_ip,username,password,netconf_payload_xml)
    # 将返回的结果转换成字典
    xmldict = xmltodict.parse(result_xml)
    # 提取字典中的CPU利用率
    return xmldict['rpc-reply']['data']['cpu-usage']['cpu-utilization'][time_interval]


if __name__ == '__main__':
    # 获取设备登录信息
    device = netconf_devices['c8kv1']
    device_ip = device['ip']
    username = device['username']
    password = device['password']

    cpu_usage = monitor_cpu(device_ip, username, password, monitor_type='5s')
    print(f'CPU利用率: {cpu_usage}%')