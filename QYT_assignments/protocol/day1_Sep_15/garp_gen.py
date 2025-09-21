#!/usr/bin/env python3
from kamene.all import ARP, Ether, sendp
from netifaces import ifaddresses, AF_LINK
import time, logging
logging.getLogger('kamene.runtime').setLevel(logging.ERROR)

def get_mac_addr(ifname):
    """
    尝试获取Linux主机网卡的MAC地址

    参数：
        ifname(str): 网卡名称
    返回：
        网卡的MAC地址(str)
    """
    try:
        return ifaddresses(ifname)[AF_LINK][0]['addr']
    except ValueError:
        return None

def send_garp(ip_addr, ifname):
    """
    每3秒发送一次免费ARP响应

    参数：
        ip_addr(str): 免费ARP的源IPv4地址
        ifname(str): 发送免费ARP的网卡名称
    """
    # 获取发送免费ARP源主机的MAC地址
    sender_mac = get_mac_addr(ifname)
    # 定义目标MAC地址为二层广播地址
    dst_mac = r'ff:ff:ff:ff:ff:ff'
    # 尝试构筑免费ARP响应并每3秒发送一次
    try:
        while True:
            sendp(Ether(src=sender_mac, dst=dst_mac) / ARP(op=2, hwsrc=sender_mac, hwdst=sender_mac, psrc=ip_addr, pdst=ip_addr),
                iface = ifname,
                verbose=False)
            print(f'发送免费ARP数据包！IP地址：{ip_addr} 本机MAC地址：{sender_mac}')
            time.sleep(3)
    except Exception as emsg:
        print(f'发生错误：{emsg}')
        return
    except KeyboardInterrupt:
        print('\n检测到用户发送Ctrl+C, 程序终止运行。')


if __name__ == '__main__':
    send_garp('10.10.1.101', 'ens192')