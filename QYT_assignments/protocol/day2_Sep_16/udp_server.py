#!/usr/bin/env python3.11
import socket
import sys
import struct
import hashlib
import pickle

from kamene.all import Key

# 绑定地址到UDP端口
address = ('0.0.0.0', 6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print('UDP服务器就绪！等待客户数据！')
while True:
    try:
        # 接收数据[注意：此处限制了发送大小为512]
        recv_source_data = s.recvfrom(512)
        # 解析发送数据与socket信息 (源地址,原端口)
        rdata, addr = recv_source_data
        # 解析2字节的版本号
        ver_num = struct.unpack('>H', rdata[0:2])[0]
        # 解析2字节的类型
        pkt_type = struct.unpack('>H', rdata[2:4])[0]
        # 解析4字节的ID号
        seq_id = struct.unpack('>I', rdata[4:8])[0]
        # 解析8字节的长度
        length = struct.unpack('>Q', rdata[8:16])[0]
        # 提取MD5值
        md5_value = rdata[-16:]
        # 计算数据部分的长度，数据报总长度减去2字节版本号、2字节类型、4字节ID、8字节长度和16字节MD5值
        data_length = len(rdata) - 32
        
        # 解析UDP报文的数据部分
        # UDP首部总长度为16字节，最后MD5值为16字节
        data = rdata[16:-16]

        # 验证MD5哈希值
        all_received_data = str(ver_num).encode() + str(pkt_type).encode() + str(seq_id).encode() + str(length).encode() + data
        md5_recv = hashlib.md5(all_received_data).digest()

        # 如果本地计算的MD5值等于发送过来的MD5值        
        if md5_recv == md5_value:
            print('=' * 80)
            print('{0:<30}:{1:<30}'.format('数据源自于', str(addr)))
            print('{0:<30}:{1:<30}'.format('数据序列号', seq_id))
            print('{0:<30}:{1:<30}'.format('数据长度为', length))
            print('{0:<30}:{1:<30}'.format('数据内容为', str(pickle.loads(data))))
        else:
            print('MD5校验错误！')
    except KeyboardInterrupt:
        sys.exit()