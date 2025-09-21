#!/usr/bin/env python3.11

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from pathlib import Path
import datetime
import os

tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))

sql_dir = f'{Path(__file__).parent}{os.sep}sqlite3'

db_file_name = f'{sql_dir}{os.sep}sqlalchemy_rtr_monit_sqlite3.db'

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False')

Base = declarative_base()

class RouterMonitor(Base):
    __tablename__ = 'router_monitor'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    cpu_usage_percent = Column(Integer, nullable=False)
    mem_use = Column(Integer, nullable=False)
    mem_free = Column(Integer, nullable=False)

    record_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f'{self.__class__.__name__}(Router: {self.device_ip}) ' \
               f'| Datetime: {self.record_datetime} ' \
               f'| CPU_Usage_Percent: {self.cpu_usage_percent} ' \
               f'| MEM Use: {self.mem_use} ' \
               f'| MEM Free": {self.mem_free}' 

if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)