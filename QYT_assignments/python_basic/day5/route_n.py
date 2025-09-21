import os
import re

# 执行并返回命令的结果
route_n_result = os.popen("route -n").read() 

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

# 将匹配到的结果赋值给一个变量
result = route_pattern.search(route_n_result)

# 为网关地址定义变量并赋值匹配结果中对应的值
gw_ip_addr = result.group('gateway')

# 打印结果
print(f'网关为:{gw_ip_addr}')
