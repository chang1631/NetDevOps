#!/usr/bin/env python3
from netmiko import Netmiko

def netmiko_show_cred(host,
                        username,
                        password,
                        cmd,
                        device_type='cisco_ios',
                        enable='Cisc0123',
                        verbose=False,
                        ssh_port=22
                        ):
    """
    根据cmd获取单台设备的相关信息

    参数：
        host(str): 设备的管理用IP地址
        username(str): 设备的管理员用户名
        password(str): 设备的管理员密码
        cmd(str): 命令
        device_type(str): 设备类型
        enable(str): Enable密码
        verbose(boolean): 控制台消息输出开关
        ssh_port(int): SSH端口号
    返回：
        设备的配置信息
    """
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'secret': enable,
                    'port': ssh_port
    }
    try:
        net_connect = Netmiko(**device_info)
        result = net_connect.send_command(cmd,
                                          use_textfsm=False
                                          )
        net_connect.disconnect()
        return result
    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return