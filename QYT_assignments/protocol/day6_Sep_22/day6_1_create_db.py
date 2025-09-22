#!/usr/bin/env python3.11

from sqlalchemy import BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from pathlib import Path
import datetime
import os

# 设置db文件得存储路径
db_dir = f'{Path(__file__).parent}{os.sep}db_dir{os.sep}'
db_file_name = f'{db_dir}sqlalchemy_iface_monit_sqlite3.db'

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

Base = declarative_base()

class InterfaceMonitor(Base):
    __tablename__= 'interface_monitor'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    interface_name = Column(String(64), nullable=False)
    in_bytes = Column(BigInteger, nullable=False)
    out_bytes = Column(BigInteger, nullable=False)

    record_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f'{self.__class__.__name__}(路由器IP: {self.device_ip}) ' \
               f'| 时间: {self.record_datetime} ' \
               f'| 接口名称: {self.interface_name} ' \
               f'| 入口字节数: {self.in_bytes} ' \
               f'| 出口字节数: {self.out_bytes} ' \

if __name__ == '__main__':
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    Base.metadata.create_all(engine, checkfirst=True)