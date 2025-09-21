import re

conn_str = 'TCP server 172.16.1.101:443 localserver 172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

#为IP地址端口定义pattern
ipv4_port = r'\d{1,3}(?:\.\d{1,3}){3}\:\d+'

#通过compile方法定义正则表达式的pattern
pattern = re.compile(
    r'^(?P<protocol>\S+)\s+'
    rf'(?P<server_title>\S+)\s+(?P<server_ip_port>{ipv4_port})\s+'
    rf'(?P<local_server_title>\S+)\s+(?P<localserver_ip_port>{ipv4_port})\,\s+'
    r'(?P<status>\S+)\s+(?P<status_hour>\d+)\:(?P<status_min>\d+)\:(?P<status_sec>\d+)\,\s+'
    r'(?P<bytes_title>\S+)\s+(?P<bytes_count>\d+)\,\s+'
    r'(?P<flags_title>\S+)\s+(?P<flags>\S+)$'
)

#将匹配到的结果赋值给一个变量
result = pattern.match(conn_str)

#分别为协议、server的IP信息、会话状态和时间、bytes和flags定义变量并赋值匹配结果中对应的值
protocol = result.group('protocol')
server_title = result.group('server_title')
server_ip_port = result.group('server_ip_port')
local_server_title = result.group('local_server_title')
local_server_ip_port = result.group('localserver_ip_port')
status = result.group('status')
hour = result.group('status_hour')
min = result.group('status_min')
sec = result.group('status_sec')
status_time = f'{hour:<2}小时 {min}分钟 {sec}秒'
byte_title = result.group('bytes_title')
bytes = result.group('bytes_count')
flags_title = result.group('flags_title')
flags = result.group('flags')

#进行格式化打印
print('='*50)
print('{:<20}{:1}{:<15}'.format('protocol', ': ', protocol))
print('{:<20}{:1}{:<15}'.format(server_title, ': ', server_ip_port))
print('{:<20}{:1}{:<15}'.format(local_server_title, ': ', local_server_ip_port))
print('{:<20}{:1}{:<15}'.format(status, ': ', status_time))
print('{:<20}{:1}{:<15}'.format(byte_title, ': ', bytes))
print('{:<20}{:1}{:<15}'.format(flags_title, ': ', flags))