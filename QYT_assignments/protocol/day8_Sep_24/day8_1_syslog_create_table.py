#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime
import os, sys

from pathlib import Path

parrent_dir = Path(__file__).parent
filename = 'sqlalchemy_syslog_sqlite3.db'

# 设置数据库文件路径及文件名
db_file_name = f'{parrent_dir}{os.sep}syslog_sqldb{os.sep}sqlalchemy_syslog_sqlite3.db'

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False',
                           # echo=True
                           )

Base = declarative_base()

class Syslog(Base):
    __tablename__ = 'syslog'

    id = Column(Integer, primary_key=True)
    device_name = Column(String(64), nullable=False)
    device_ip = Column(String(64), nullable=False)
    facility = Column(Integer, nullable=False)
    facility_name = Column(String(64), nullable=False)
    severity_level = Column(Integer, nullable=False)
    severity_level_name = Column(String(64), nullable=False)
    logid = Column(Integer, nullable=False)
    log_source = Column(String(64), nullable=False)
    description = Column(String(128), nullable=False)
    text = Column(String(1024), nullable=False)
    time = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} " \
               f"| Datetime: {self.time} " \
               f"| Severity Name: {self.severity_level_name})"


if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)