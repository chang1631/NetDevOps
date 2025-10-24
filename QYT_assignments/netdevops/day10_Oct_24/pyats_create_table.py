#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, JSON
import datetime
import os, sys

from pathlib import Path

parrent_dir = Path(__file__).parent
filename = 'sqlalchemy_pyats.db'

# 设置数据库文件路径及文件名
db_file_name = f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}{filename}'

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

Base = declarative_base()

# 记录设备的OSPF和路由状态表
class PyatsOSPF(Base):
    __tablename__ = 'pyats_ospf'

    id = Column(Integer, primary_key=True)
    device_name = Column(String(64), nullable=False)
    device_ip = Column(String(64), nullable=False)
    ospf_status = Column(JSON, nullable=False)
    route_table_status = Column(JSON, nullable=False)
    record_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(Device_Name: {self.device_name} " \
               f"| Device_IP: {self.device_ip} " \
               f"| Datetime: {self.record_datetime})"


if __name__ == '__main__':
    # 删除旧的同名数据库文件
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    Base.metadata.create_all(engine, checkfirst=True)