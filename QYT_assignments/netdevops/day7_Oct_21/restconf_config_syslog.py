#!/usr/bin/env python3
from request_info import client, headers, devices
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def conf_syslog(device_ip, username, password, severity, hostip):
    """
    通过RESTCONF配置SYSLOG服务器

    参数：
        ip(str): 设备的管理IPv4地址
        username(str): 用户名
        password(str): 密码
        severity(int): 日志的严重级别
        hostip(str): syslog服务器IPv4地址
    """

    # 构建SYSLOG配置相关数据的字典
    syslog_config_data = {"Cisco-IOS-XE-native:logging": {
                            "trap": {
                                "severity": severity},
                            "hostip": hostip
                            }}
    # Logging相关的URL
    url = f'https://{device_ip}/restconf/data//Cisco-IOS-XE-native:native/logging'
    # 发送配置SYSLOG的RESTCONF请求
    rest_req = client.put(url,
                          headers=headers,
                          auth=HTTPBasicAuth(username, password),
                          json = syslog_config_data,
                          verify=False)
    # 打印HTTP状态码和Response的JSON数据
    if rest_req.ok:
        print(rest_req.status_code)
        print(f'Syslog配置成功!')
    else:
        print(rest_req.text)

if __name__ == "__main__":
    device = devices['c8kv1']
    router_ip =  device['ip']
    username = device['username']
    password = device['password']

    # 定义SYSLOG的severity和服务器IPv4地址
    severity = 5
    hostip = '10.10.1.234'

    conf_syslog(router_ip, username, password, severity, hostip)