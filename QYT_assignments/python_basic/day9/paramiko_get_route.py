# 从第一题创建的paramiko_ssh.py中导入函数qytang_ssh
from paramiko_ssh import qytang_ssh
import re

def ssh_get_route(ip, username, password, port=22):
    """
    通过SSH远程连接到Linux主机查询路由信息并提取网关IP地址
    返回网关IP地址
    """
    # 定义0.0.0.0的IPv4地址和网关IPv4地址的pattern
    all_zero_ip = r'0(?:\.0){3}'
    ip_addr = r'\d{1,3}(?:\.\d{1,3}){3}'
    # 定义默认路由条目的pattern，匹配Destination和Genmask为0.0.0.0且Flags为UG的路由条目
    route_pattern = re.compile(
        fr'(?P<destination>{all_zero_ip})\s+'
        fr'(?P<gateway>{ip_addr})\s+'
        fr'(?P<genmask>{all_zero_ip})\s+'
        r'(?P<flags>UG)\s+'
        r'(?P<metric>\d+)\s+'
        r'(?P<ref>\d+)\s+'
        r'(?P<use>\d+)\s+'
        r'(?P<iface>\S+)\s+'
    )
    # 调用函数qytang_ssh通过SSH远程登录到Linux主机查询路由信息并将结果赋值给一个变量
    route_n_result = qytang_ssh(ip, username, password, port, cmd='route -n')
    # 将正则表达式匹配到的网关IP地址赋值给一个变量
    gw_ip_addr = route_pattern.search(route_n_result).group('gateway')

    return gw_ip_addr

    

if __name__ == '__main__':
    gw_ipaddr = ssh_get_route('10.10.1.222', 'root', 'cisco123')
    print(f'网关为:\n{gw_ipaddr}')