import random

#定义一个列表用于存储随机生成的IPv4地址的数字
octets = []

#初始化while循环的index值
index= 0

#通过循环生成4个1-255之间的随机数并依次将其转换成字符串后添加至octets列表
while index < 4:
    octets.append(str(random.randint(1,255)))
    index += 1

#将拼接后的IPv4地址赋值给变量ipv4_addr
ipv4_addr = '.'.join(octets)

print(ipv4_addr)