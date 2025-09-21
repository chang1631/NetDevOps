import re

asa_conn = "TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO\n \
TCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"

asa_dict = {}

# 为IPv4地址定义pattern
ipv4_addr = r'\d{1,3}(?:\.\d{1,3}){3}'

# 通过compile定义pattern
pattern = re.compile(
    # 匹配开头协议的关键字TCP或UDP等(多行输出在开头会出现空格)
    r'^(?:\s)*(?:\S+)\s+'
    # 匹配源目IP地址和端口
    rf'(?:\S+\s+)(?P<src_ip>{ipv4_addr})\:(?P<src_port>\d+)\s+'
    rf'(?:\S+\s+)(?P<dst_ip>{ipv4_addr})\:(?P<dst_port>\d+)\,\s+'
    # 匹配idle信息
    r'(?:\S+\s+\d+\:\d+\:\d+)\,\s+'
    # 匹配bytes和flags
    r'(?:bytes)\s+(?P<bytes>\d+)\,\s+'
    r'(?:flags)\s+(?P<flags>\S+)$'
)

for conn in asa_conn.split('\n'):
    re_result = pattern.match(conn)
    # 为源IP和端口、目的IP和端口、字节数和flags定义变量并根据匹配到的结果进行赋值
    src_ip = re_result.group('src_ip')
    src_port = re_result.group('src_port')
    dst_ip = re_result.group('dst_ip')
    dst_port = re_result.group('dst_port')
    bytes_count = re_result.group('bytes')
    flags = re_result.group('flags')
    asa_dict[src_ip, src_port, dst_ip, dst_port]= (bytes_count, flags)
print('打印分析后的字典! \n')
print(asa_dict)

src = 'src'
src_ip = 'src_ip'
dst = 'dst'
dst_ip = 'dst_ip'
bytes_name = 'bytes'
flags = 'flags'
format_str1 = r'{0:^12}:{1:^15}|{2:^12}:{3:^15}|{4:^12}:{5:^15}|{6:^12}:{7:^15}'
format_str2 = r'{0:^12}:{1:^15}|{2:^12}:{3:^15}'
print('\n格式化打印输出\n')

for key, value in asa_dict.items():
    print(format_str1.format(src, key[0], src_ip, key[1], dst, key[2], dst_ip, key[3]))
    print(format_str2.format(bytes_name, value[0], flags, value[1]))
    print('='*115)