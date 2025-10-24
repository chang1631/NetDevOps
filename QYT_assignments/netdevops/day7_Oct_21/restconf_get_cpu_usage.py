#!/usr/bin/env python3
from request_info import client, headers, devices
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def monitor_cpu(device_ip, username, password, monitor_type='5s'):
    """
    通过RESTCONF获取指定时间间隔内的设备CPU利用率

    参数：
        ip(str): 设备的管理IPv4地址
        username(str): 用户名
        password(str): 密码
        monitor_type(str): 时间间隔
    返回：
        CPU利用率(int)
    """
    # 根据monitor_type定义time_interval的值
    if monitor_type == '1m':
        time_interval = 'one-minute'
    elif monitor_type == '5m':
        time_interval = 'five-minutes'
    else:
        time_interval = 'five-seconds'
    # CPU利用率的URL
    url = f'https://{device_ip}/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization/{time_interval}'
    # 发送获取CPU利用率的RESTCONF请求
    rest_req = client.get(url,
                          headers=headers,
                          auth=HTTPBasicAuth(username, password),
                          verify=False)
    # 返回HTTP Response的JSON数据
    if rest_req.ok:
        return rest_req.json().get(f'Cisco-IOS-XE-process-cpu-oper:{time_interval}')
    else:
        return '获取数据失败'

if __name__ == "__main__":
    device = devices['c8kv1']
    router_ip =  device['ip']
    username = device['username']
    password = device['password']
    cpu_usage = monitor_cpu(router_ip, username, password, '5s')

    # 如果返回的是int整数则打印CPU利用率，否则打印失败消息
    print(f'CPU利用率: {cpu_usage}%') if isinstance(cpu_usage, int) else print(cpu_usage)