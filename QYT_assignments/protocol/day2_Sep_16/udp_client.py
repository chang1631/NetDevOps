#!/usr/bin/env python3.11
import socket
import struct
import hashlib
import pickle

def udp_send_data(ip, port, data_list):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id = 1
    for x in data_list:
        # ---header设计---
        # 2字节 版本1
        # 2字节 类型1为请求 类型2为响应(由于是UDP单向流量！所有此次试验只有请求)
        # 4字节 ID号
        # 8字节 长度

        # |  2  |  2  |    4   |        8       |
        # | ver | type|   ID   |      len       |

        # ---变长数据部分---总长度控制为512
        # 使用pickle转换数据

        # ---HASH校验---
        # 16字节 MD5值

        # 把Python数据或者对象Pickle成为二进制数据
        send_data = pickle.dumps(x)

        # 由于Server端限制接收UDP数据总长度为512字节，所以发送的数据部分不应超过480字节
        # 512字节总长度 - 16字节首部 - 16字节的MD值 = 480字节
        if len(send_data) > 480:
            print('数据部分字节数过长，超过UDP报文总长度512字节限制！')
            continue
        
        # 计算MD5哈希值
        all_data = str(version).encode() + str(pkt_type).encode() + str(seq_id).encode() + str(len(send_data)).encode() + send_data  
        hash_value = hashlib.md5(all_data).digest()

        # 按照头部设计构建头部
        endian = '>'      # 按网络标准的字节序
        header_ver = 'H'  # 2字节版本号
        header_type = 'H' # 2字节类型
        header_id = 'I'   # 4字节ID号
        header_len = 'Q'  # 8字节长度
        datagram = f'{len(send_data)}s' # 可变长的数据部分
        md5_hash = '16s'  # 16字节 MD5值

        # 拼接 头部+发送数据+MD5值， 然后发送到目的服务器
        udp_dg_format = endian + header_ver + header_type + header_id + header_len + datagram + md5_hash
        packed_data = struct.pack(udp_dg_format, version, pkt_type, seq_id, len(send_data), send_data, hash_value)
        s.sendto(packed_data, address)

        seq_id += 1
    s.close()


if __name__ == '__main__':
    from datetime import datetime
    user_data = ['乾颐堂', [1, 'qytang', 3], {'qytang':1 , 'test':3}, {'datetime': datetime.now()}]
    udp_send_data('10.10.1.200', 6666, user_data)