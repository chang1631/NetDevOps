#!/usr/bin/env python3.11
import sys, asyncio
from pathlib import Path
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy import create_engine

current_dir = Path(__file__).parent.parent
sys.path.insert(1, str(current_dir))

from day4_Sep_18.day4_1_create_db import RouterMonitor, engine, db_file_name
from day4_Sep_18.day4_snmp_get_all import snmpv3_get_all

print(db_file_name)

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')



def get_info_writedb(device_list, username, auth_key,priv_key):
    all_dict_list = asyncio.run(snmpv3_get_all(device_list, username, auth_key,priv_key))
    records = []
    for dict in all_dict_list:
        # 如果SNMP GET执行失败会返回None，需要进行判断
        if dict:
            records.append(RouterMonitor(**dict))
    session.add_all(records)
    session.commit()
        

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    devices = ['10.10.1.101','10.10.1.102']
    username = 'qytanguser'
    qytang_auth_key = 'Cisc0123'
    qytang_priv_key = 'Cisc0123'
    get_info_writedb(devices, username, qytang_auth_key, qytang_priv_key)
