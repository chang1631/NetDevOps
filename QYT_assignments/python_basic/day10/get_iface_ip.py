from ping_tester import qytang_ping
from ssh_operator import qytang_ssh
import re
import pprint as pp
from ipaddress import ip_address

def qytang_get_if(*ips, username='admin', password='Cisc0123', port=22):
    """
    对通过Ping连通性测试的设备进行SSH登录并收采集接口信息
    参数：
        *ips(str): IP地址
        username(str): 用户名，默认为admin
        password(str): 密码，默认为Cisc0123
        port(int): SSH端口号，默认值为22
    返回：
        接口信息字典
    """
    device_if_dict = {}
    # 为接口名称和IP地址定义正则表达式的pattern
    iface_pattern = r'([A-Z]\S+\d+)\s+(\d{1,3}(?:\.\d{1,3}){3})'
    for ip_addr in ips:
        try:
            # 先验证IPv4地址是否合规
            ip_address(ip_addr)
            ping_result = qytang_ping(ip_addr)
            # 如果PING测试通过则尝试SSH登录并采集接口信息
            if ping_result:
                ssh_result = qytang_ssh(ip_addr, username, password, port, cmd='show ip int brief')
                if ssh_result is not False:
                    iface_list = re.findall(iface_pattern,ssh_result)
                    # 创建一个空字典用于存储接口及IPv4地址信息 {'GigabitEthernet1': '10.10.1.101'}
                    iface_dict = {}
                    for iface_name, iface_ipaddr in iface_list:
                        iface_dict.update({iface_name:iface_ipaddr})          
                    # 以设备的管理IP地址作为键，接口信息(字典)作为值更新到字典device_if_dict中
                    device_if_dict.update({ip_addr:iface_dict})
        except ValueError:
            print(f'{ip_addr}不是一个合规的IPv4地址！\n')     
    return device_if_dict



if __name__ == '__main__':
    # 10.10.1.110是一个不存在的IPv4地址
    # 10.10.1.222是一台Linux主机，不会返回命令show ip int brief的执行结果
    # 10.10.1.999是一个不合规的IPv4地址
    res = qytang_get_if('10.10.1.101', '10.10.1.110','10.10.1.222', '10.10.1.102', '10.10.1.999')
    print('设备接口信息采集结果:\n')
    pp.pprint(res, indent=4)

# if __name__ == '__main__':
#     # 传入一个非标准的SSH端口号port = 2025
#     res = qytang_get_if('10.10.1.101', '10.10.1.110','10.10.1.222', '10.10.1.102', port = 2025)
#     print('设备接口信息采集结果:\n')
#     pp.pprint(res, indent=4)

# if __name__ == '__main__':
#     # 传入一个错误的密码password = 'abc123'
#     res = qytang_get_if('10.10.1.101', '10.10.1.222', '10.10.1.102', password = 'abc123')
#     print('设备接口信息采集结果:\n')
#     pp.pprint(res, indent=4)