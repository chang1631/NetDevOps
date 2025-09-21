import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from kamene.all import *

def qytang_ping(ip):
    """
    构建ping数据包并测试设备连通性
    参数：
        ip(str):设备的IP地址 
    返回:
        Boolean：True或False
    """
    ping_pkt = IP(dst=ip)/ICMP()
    ping_result = sr1(ping_pkt, timeout=2, verbose=False)
    # 如果接收到了ICMP的回包且类型为echo reply则说明可以ping通
    if ping_result and ping_result.haslayer(ICMP) and ping_result[ICMP].type == 0:
        return True
    else:
        print(f'设备 {ip} 无法ping通，请检查网络连接或设备状态！\n')
        return False

if __name__ == '__main__':
    # 定义目的地址为网关的IP地址
    dst_ip = '10.10.1.254'
    result = qytang_ping(dst_ip)
    if result:
        print(f'{dst_ip} 通')
    else:
        print(f'{dst_ip} 不通')
