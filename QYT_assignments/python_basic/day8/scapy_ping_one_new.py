import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from kamene.all import *

def qytang_ping(ip):
    # 构建ping数据包并将返回的结果赋值给一个变量
    ping_pkt = IP(dst=ip)/ICMP()
    ping_result = sr1(ping_pkt, timeout=2, verbose=False)
    if ping_result:
        return True
    else:
        return False

if __name__ == '__main__':
    # 定义目的地址为网关的IP地址
    dst_ip = '192.168.1.2'
    result = qytang_ping(dst_ip)
    if result:
        print(f'{dst_ip} 通')
    else:
        print(f'{dst_ip} 不通')