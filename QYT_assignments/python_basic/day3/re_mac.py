import re

str1 = '166    54a2.74f7.0326    DYNAMIC     Gi1/0/11'

#为MAC地址定义pattern
mac_addr = r'[0-9a-fA-F]{4}(?:\.[0-9a-fA-F]{4}){2}'


#通过compile方法定义pattern
pattern = re.compile(
    r'^(?P<vlan_id>\d+)\s+'
    rf'(?P<mac_address>{mac_addr})\s+'
    r'(?P<type>\S+)\s+'
    r'(?P<interface>\S+)$'
)

#将匹配到的结果赋值给一个变量
result = pattern.match(str1)

#分别为VLANID、MAC地址、类型和接口定义变量并赋值匹配结果中对应的值
vlan_id = result.group('vlan_id')
mac_address = result.group('mac_address')
type = result.group('type')
interface = result.group('interface')

#进行格式化打印
print('='*50)
print('{:<12}{:1}{:<15}'.format('VLAN ID', ': ', vlan_id))
print('{:<12}{:1}{:<15}'.format('MAC', ': ', mac_address))
print('{:<12}{:1}{:<15}'.format('Type', ': ', type))
print('{:<12}{:1}{:<15}'.format('Interface', ': ', interface))
