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

def conf_syslog(device_ip, username, password, severity, hostip):
    """
    通过NETCONF RPC配置SYSLOG

    参数：
        ip(str): 设备的管理IPv4地址
        username(str): 用户名
        password(str): 密码
        severity(int): 日志的严重级别
        hostip(str): syslog服务器IPv4地址
    """
    # 打开logging_config模板并进行渲染
    with open(xml_path + 'logging_config.jinja2', encoding='utf-8') as f:
        netconf_template = Template(f.read())
    netconf_payload_xml = netconf_template.render(severity=severity, hostip=hostip)
    # 发送配置SYSLOG的NETCONF RPC请求
    try:
        result_xml = netconfig_request(device_ip,username,password,netconf_payload_xml)
        # 将返回的结果转换成字典
        xmldict = xmltodict.parse(result_xml)
        # 如果字典中存在键'ok'，则打印配置成功消息
        if xmldict.get('rpc-reply') is not None and 'ok' in xmldict['rpc-reply']:
            print(f'Syslog配置成功!')
        # 否则打印失败消息
        elif xmldict.get('rpc-error') is not None:
            error_message_text = xmldict['rpc-error']['error-message']['#text']
            print(f'Syslog配置失败: {error_message_text}')
    # 处理其他异常
    except Exception as e:
        print(f'发生未知错误:str(e)')
    

if __name__ == '__main__':
    # 获取设备登录信息
    device = netconf_devices['c8kv1']
    device_ip = device['ip']
    username = device['username']
    password = device['password']

    syslog_config = conf_syslog(device_ip, username, password, 7, "10.1.1.60")