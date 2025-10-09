#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pathlib import Path
import os,sys

# 将当前的路径添加至Python解释器的路劲列表
parrent_dir = Path(__file__).parent
sys.path.append(str(parrent_dir))

from day7_1_psql_createdb import Router, Interface, OSPFProcess, Area, OSPFNetwork, CPUUsage, engine

Session = sessionmaker(bind=engine)
session = Session()

# 设备接口信息
c8kv1_ifs = [{'ifname': 'GigabitEthernet2', 'ip': '20.1.1.101', 'mask': '255.255.255.0'},
             {'ifname': 'Loopback0 ', 'ip': '1.1.1.1', 'mask': '255.255.255.255'}]

c8kv2_ifs = [{'ifname': 'GigabitEthernet2', 'ip': '20.1.1.102', 'mask': '255.255.255.0'},
             {'ifname': 'Loopback0 ', 'ip': '2.2.2.2', 'mask': '255.255.255.255'}]

# 设备OSPF信息
c8kv1_ospf = {'process_id': 1,
              'router_id': '1.1.1.1',
              'areas': [{'area_id':0, 'network': [{'ip': '20.1.1.0', 'wildmask': '0.0.0.255'},
                                                  {'ip': '1.1.1.1', 'wildmask': '0.0.0.0'}]}]}

c8kv2_ospf = {'process_id': 1,
              'router_id': '2.2.2.2',
              'areas': [{'area_id':0, 'network': [{'ip': '20.1.1.0', 'wildmask': '0.0.0.255'},
                                                  {'ip': '2.2.2.2', 'wildmask': '0.0.0.0'}]}]}

# 设备的管理员账户
username = 'admin'
password = 'Cisc0123'

# 讲配置数据进行汇总
all_network_data = [{'ip': '10.10.1.101',
                     'routernam': 'C8kv1',
                     'interface': c8kv1_ifs,
                     'ospf': c8kv1_ospf,
                     'username': username,
                     'password': password},
                    {'ip': '10.10.1.102',
                     'routernam': 'C8kv2',
                     'interface': c8kv2_ifs,
                     'ospf': c8kv2_ospf,
                     'username': username,
                     'password': password}]

# 遍历数据集合并写入路由器的相关数据至数据库
for device_data in all_network_data:
    device_ip = device_data['ip']
    device_name = device_data['routernam']
    iface_list = device_data['interface']
    ospf_dict = device_data['ospf']
    username = device_data['username']
    password = device_data['password']

    # 写入数据至表Router
    router_device = Router(router_name=device_name, ip=device_ip,username=username,password=password)
    session.add(router_device)

    # 写入数据至表Interface
    for iface_dict in iface_list:
        iface_name = iface_dict['ifname']
        ip = iface_dict['ip']
        mask = iface_dict['mask']

        interface = Interface(router=router_device, interface_name= iface_name, ip=ip, mask=mask)
        session.add(interface)
    
    # 写入数据至表OSPF Process
    ospf_dict = device_data['ospf']
    ospf_process = OSPFProcess(router=router_device, 
                               processid=ospf_dict['process_id'],
                               routerid=ospf_dict['router_id'])
    session.add(ospf_process)
                    
    # 写入数据至表Area和OSPF Network
    area_list = device_data['ospf']['areas']
    

    for ospf_area in area_list:
        area_id = ospf_area['area_id']
        area_network_list = ospf_area['network']
        area = Area(ospf_process=ospf_process, area_id=area_id)

        session.add(area)

        for ospf_network in area_network_list:
            network = ospf_network['ip']
            wildmask = ospf_network['wildmask']
            network_data = OSPFNetwork(area=area, network=network, wildmask=wildmask)

            session.add(network_data)

session.commit()