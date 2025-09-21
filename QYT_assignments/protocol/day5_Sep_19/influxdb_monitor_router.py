#!/usr/bin/env python 3.11
from pathlib import Path
from influxdb import InfluxDBClient
import sys, datetime, asyncio

file_dir_path = Path(__file__).parent
project_dir_path = Path(__file__).parent.parent

# 将当前项目路径添加至Python解释器解析路径中
sys.path.insert(0, str(project_dir_path))

# 导入第四天作业的snmpv3_get_all模块
from day4_Sep_18.day4_snmp_get_all import snmpv3_get_all

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

# ===========写入CPU和内存利用率数据===========
# 调用异步函数snmpv3_get_all获取所有设备的CPU和内存利用率数据
all_results = asyncio.run(snmpv3_get_all(devices, username, qytang_auth_key, qytang_priv_key))

# 获取当前时间
current_time = datetime.datetime.now(datetime.timezone.utc).isoformat('T')

# 每个设备的CPU和内存利用率数据都存储于一个独立的字典中
# 由于有多台设备，所以需要定义一个列表用于存储每个设备的监控数据所产生的字典
cpu_mem_body = []
for getall_result in all_results:
    cpu_mem_dict =  {
                        'measurement': 'router_monitor',  # 类似表表名
                        'time': current_time,
                        'tags':{                          # 过滤标签
                            'device_ip': getall_result.get('device_ip'),
                            'device_type': 'IOS-XE'
                        },
                        'fields': {                       # 数据字段
                            'cpu_usage': getall_result.get('cpu_usage_percent'),
                            'mem_usage': getall_result.get('mem_use'),
                            'mem_free': getall_result.get('mem_free'),
                        },
                    }
    cpu_mem_body.append(cpu_mem_dict)

# 写入InfluxDB数据库
client.write_points(cpu_mem_body)




