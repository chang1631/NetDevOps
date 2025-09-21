import re

str1 = 'Port-channel1.189          192.168.189.254  YES     CONFIG   up                       up '

#为IP地址定义pattern
ipv4_addr = r'\d{1,3}(?:\.\d{1,3}){3}'

#通过compile方法定义正则表达式的pattern
pattern = re.compile(
    r'^(?P<interface>\S+)\s+'
    rf'(?P<ipv4_address>{ipv4_addr})\s+'
    r'(?P<ok>\w+)\s+'
    r'(?P<method>\w+)\s+'
    r'(?P<status>\w+)\s+'
    r'(?P<protocol>\w+)\s+$'
)

#将匹配到的结果赋值给一个变量
match_res = pattern.match(str1)

#分别为接口、IP地址和状态定义变量并赋值匹配结果中对应的值
interface = match_res.group('interface')
ipv4_address = match_res.group('ipv4_address')
status = match_res.group('status')

#进行格式化打印
print('-'*100)
print('{:<10}{:1}{:<15}'.format('接口', ': ', interface))
print('{:<10}{:1}{:<15}'.format('IP地址', ': ', ipv4_address))
print('{:<10}{:1}{:<15}'.format('状态', ': ', status))
