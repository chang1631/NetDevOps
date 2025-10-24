#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker

from pyats_create_table import engine, PyatsOSPF

Session = sessionmaker(bind=engine)
session = Session()

def write_ospf_status_db(ospf_data_dict):        
    """
    创建OSPF记录并写入数据库

    参数:
        ospf_data_dict(dict): OSPF状态数据
    """
    ospf_record = PyatsOSPF(**ospf_data_dict)
    session.add(ospf_record)
    session.commit()