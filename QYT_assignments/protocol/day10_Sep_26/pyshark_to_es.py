#!/usr/bin/env python3
import pyshark, os
from datetime import timezone, timedelta
# Elasticsearch Python 客户端，用于把数据写入 ES。
from elasticsearch import Elasticsearch

from pathlib import Path
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 设置时区为UTC
tzutc_0 = timezone(timedelta(hours=0))

# 连接到ElasticSearch
es = Elasticsearch('http://10.10.1.200:9200')

# pcap文件所在路径
pcap_file = f'{parrent_dir}{os.sep}pcap_files{os.sep}day10_lab.pcap'

# 创建一个 FileCapture 对象，用于逐包读取 pcap 文件
cap = pyshark.FileCapture(pcap_file, keep_packets=False)

# 初始化数据索引值
i = 1

def write_pkt_es(pkt):
    """
    处理pcap数据包
    
    参数：
        pkt(obj): 要处理的数据包对象
    """
    # 申明数据索引值i为全局变量
    global i

    # 定义一个字典用于临时存储数据包中的所有字段
    pkt_dict = {}

    # 使用Pyshark遍历数据包的所有协议层（eth、ip、tcp 等），提取字段并存到 pkt_dict
    # pkt.__dict__.get('layers') -> [eth, ip, tcp, http ...]
    # 每个 layer 里有很多字段 -> {'ip.src': '192.168.1.10', 'ip.dst': '8.8.8.8', ....}
    for layer in pkt.__dict__.get('layers'):
        pkt_dict.update(layer.__dict__.get('_all_fields'))

    # 定义一个字典用于存储清洗后的字段
    pkt_dict_final = {}
    # 把字段分割成字典
    for key, value in pkt_dict.items():
        # 略过空键
        if key == '':
            continue
        else:
            # 替换key名称中的'.'为'_'，避免 Elasticsearch 解析出错。
            pkt_dict_final[key.replace('.', '_')] = value
    
    # 切换时区，记录抓包时间（转成 UTC + ISO8601 格式）
    pkt_dict_final.update({'sniff_time': pkt.sniff_time.astimezone(tzutc_0).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'})
    # 记录最高层协议（如 TCP、HTTP、TLS）
    pkt_dict_final.update({'highest_layer': pkt.highest_layer})

    try:
        # 把ip_len转换成整数
        ip_len = int(pkt_dict_final.get('ip_len'))
        pkt_dict_final['ip_len'] = ip_len

        # 添加数据到索引(默认值为1)
        # 把处理好的 pkt_dict_final 作为一个文档doc写入到 Elasticsearch 索引 qyt-pyshark-index 里
        # body为最终的字典pkt_dict_final
        resp = es.index(index='qyt-pyshark-index', id=i, doc_type='doc', body=pkt_dict_final)
        print(resp['result'])

        i += 1
    except Exception:
        pass

# 遍历 pcap 文件里的每个数据包。
# 对每个包调用 write_pkt_es(pkt)，完成清洗和入库。
cap.apply_on_packets(write_pkt_es)