#!/usr/bin/env python3
from netmiko import Netmiko
import asyncio

def netmiko_config_cred(host,
                        username,
                        password,
                        cmds_list,
                        device_type='cisco_ios',
                        enable='Cisc0123',
                        verbose=False,
                        ssh_port=22
                        ):
    """
    根据配置清单cmds_list使用异步方法对单台设备进行配置

    参数：
        host(str): 设备的管理用IP地址
        username(str): 设备的管理员用户名
        password(str): 设备的管理员密码
        cmds_list(list): 配置命令列表
        device_type(str): 设备类型
        enable(str): Enable密码
        verbose(boolean): 控制台消息输出开关
        ssh_port(int): SSH端口号
    返回：
        命令执行的结果
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
        if verbose:
            output = net_connect.send_config_set(cmds_list)
            net_connect.disconnect()
            return output
        else:
            net_connect.send_config_set(cmds_list)
            net_connect.disconnect()
            return None

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return