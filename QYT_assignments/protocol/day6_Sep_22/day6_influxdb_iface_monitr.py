#!/usr/bin/env python 3.11
from pathlib import Path
from influxdb import InfluxDBClient
import sys, datetime, asyncio

file_dir_path = Path(__file__).parent
project_dir_path = Path(__file__).parent.parent

# 将当前项目路径添加至Python解释器解析路径中
sys.path.insert(0, str(project_dir_path))

# 导入snmpv3_get_all_ifaces模块
from day6_Sep_22.day6_snmp_get_all import snmpv3_get_all_ifaces

influx_srv = '10.10.1.200'
devices = ['10.10.1.101','10.10.1.102']
username = 'qytanguser'
qytang_auth_key = 'Cisc0123'
qytang_priv_key = 'Cisc0123'
influx_db = 'qytdb'
influx_port = 8086
influx_measurement = 'router_monitor'
influx_user = 'qytdbuser'
influx_password = 'Cisc0123'

# 初始化InfluxDB客户端
client = InfluxDBClient(influx_srv, influx_port, influx_user, influx_password, influx_db)
# client.query("drop measurement interface_monitor")  # 删除表

# ===========写入CPU和内存利用率数据===========
# 调用异步函数snmpv3_get_all获取所有设备的CPU和内存利用率数据
all_results = asyncio.run(snmpv3_get_all_ifaces(devices, username, qytang_auth_key, qytang_priv_key))

# 获取当前时间
# current_time = datetime.datetime.now(datetime.timezone.utc).isoformat('T')
current_time = datetime.datetime.utcnow().isoformat() + "Z"

# 每个设备的接口出栈和入栈信息分别存储于一个独立的字典中
# 存储每个接口入栈方向相关数据的字典
if_in_bytes_body = []
# 存储每个接口出栈方向相关数据的字典
if_out_bytes_body = []
# 遍历get_all_ifaces的返回结果(列表)
for result in all_results:
    # 遍历字典中的接口信息列表
    for if_info in result.get('interface_list'):
        # 如果入方向和出方向都有流量则为该接口构建入栈和出栈方向的数据字典并添加至相关列表中
        if int(if_info.get('in_bytes')) >0 and int(if_info.get('out_bytes')) > 0: 
            if_in_bytes_dict =  {
                                'measurement': 'interface_monitor',  # 类似表表名
                                'time': current_time,
                                'tags':{                          # 过滤标签
                                    'device_ip': result.get('device_ip'),
                                    'device_type': 'IOS-XE',
                                    'interface_name': if_info.get('interface_name')
                                },
                                'fields': {                       # 数据字段
                                    'in_bytes': int(if_info.get('in_bytes')),
                                },
                            }
            if_in_bytes_body.append(if_in_bytes_dict)

            if_out_bytes_dict =  {
                                'measurement': 'interface_monitor',  # 类似表表名
                                'time': current_time,
                                'tags':{                          # 过滤标签
                                    'device_ip': result.get('device_ip'),
                                    'device_type': 'IOS-XE',
                                    'interface_name': if_info.get('interface_name')
                                },
                                'fields': {                       # 数据字段
                                    'out_bytes': int(if_info.get('out_bytes')),
                                },
                            }
            if_out_bytes_body.append(if_out_bytes_dict)

# 写入InfluxDB数据库
client.write_points(if_in_bytes_body)
client.write_points(if_out_bytes_body)
