#!/usr/bin/env python3
import sys, os, asyncio

from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

parent_dir = Path(__file__).parent
# project_dir = parent_dir.parent
sys.path.insert(1, str(parent_dir))


from day6_snmp_get_all import snmpv3_get_all_ifaces
from day6_1_create_db import InterfaceMonitor, db_file_name

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False',
                       # echo=True
                       )

Session = sessionmaker(bind=engine)
session = Session()

def get_ifaces_writedb(devices, username, auth_key, priv_key):
    devcies_ifaces_dict_list =  asyncio.run(snmpv3_get_all_ifaces(devices, username, auth_key, priv_key))
    for dict in devcies_ifaces_dict_list:
        device_ifaces_dict = {}
        ip = dict.get('device_ip') 
        ifaces_list = dict.get('interface_list') 
        for iface in ifaces_list:
            device_ifaces_dict.update({
                'device_ip': ip,
                **iface
            })
            iface_monitr_record = InterfaceMonitor(**device_ifaces_dict)
            session.add(iface_monitr_record)
            session.commit()

if __name__ == '__main__':
    # ip地址与snmp community字符串
    devices = ['10.10.1.101', '10.10.1.102']
    username = "qytanguser"
    auth_key = 'Cisc0123'
    priv_key = 'Cisc0123'

    get_ifaces_writedb(devices, username, auth_key, priv_key)