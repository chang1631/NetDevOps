import os
import re

ifconfig_result = os.popen('ifconfig ' + 'ens192').read()

# 为IP地址、掩码、广播地址和MAC地址定义pattern
ipv4_pattern = r'(?:inet\s+)(\d{1,3}(?:\.\d{1,3}){3})'
netmask_pattern = r'(?:netmask\s+)(\d{1,3}(?:\.\d{1,3}){3})'
broadcast_pattern = r'(?:broadcast\s+)(\d{1,3}(?:\.\d{1,3}){3})'
mac_pattern = r'([a-fA-F0-9]{2}(?:\:[a-fA-F0-9]{2}){5})'

# 通过正则表达式找到ip、掩码、广播和mac地址
ipv4_add = re.findall(ipv4_pattern, ifconfig_result)[0]
netmask = re.findall(netmask_pattern, ifconfig_result)[0]
broadcast = re.findall(broadcast_pattern, ifconfig_result)[0]
mac_addr = re.findall(mac_pattern, ifconfig_result)[0]

# 格式化字符串
format_string = '{:<11}:{:<18}'

# 打印结果
print(format_string.format('ipv4_add', ipv4_add))
print(format_string.format('netmask', netmask))
print(format_string.format('broadcast', broadcast))
print(format_string.format('mac_addr', mac_addr))

# 产生网关的IP地址
# 将原先的IPv4基于"."拆分成一个列表
ipv4_octets = ipv4_add.split('.')

#将列表ipv4_octets的最后一个元素修改为假设的网关地址主机位并重组成字符串
ipv4_gw = ".".join(ipv4_octets[:-1] + ['254'])

# 打印网关的IP地址
print('\n我们假设网关IP地址的最后一位为254, 因此网关IP地址为:' + ipv4_gw + '\n')

# Ping网关
ping_result = os.popen('ping ' + ipv4_gw + ' -c 1').read()

re_ping_result = re.search('1\s+received',ping_result)

if re_ping_result:
    print('网关可达！')
else:
    print('网关不可达！')