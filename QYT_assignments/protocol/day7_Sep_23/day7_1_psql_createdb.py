#!/usr/bin/env python3
from sqlalchemy import create_engine, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

tzutc8 = datetime.timezone(datetime.timedelta(hours=8))

# ---------------初始化PSQL Engine---------------
engine = create_engine('postgresql+psycopg2://qytangdbuser:Cisc0123@10.10.1.200/qytangdb')

Base = declarative_base()

# 表Router
class Router(Base):
    __tablename__ = 'router'

    id = Column(Integer, primary_key=True)
    router_name = Column(String(64), nullable=False, index=True)
    ip = Column(String(64), nullable=False, index=True)
    username = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)

    # ----------定义relationshio属性----------
    # 格式：
    #   obj_name = relationship(对端类名，对端relationship的属性/变量名)

    # ----------接口----------
    interface = relationship('Interface', back_populates='router', passive_deletes=True)

    # ----------OSPF----------
    ospf_process = relationship('OSPFProcess', back_populates='router', uselist=False, passive_deletes=True)

    # ----------CPU利用率----------
    cpu_usage = relationship('CPUUsage', back_populates='router', passive_deletes=True)

    # ----------设备配置----------
    device_config = relationship('DeviceConfig', back_populates='router', passive_deletes=True)
    # 以字典的形式返回表中的数据
    def open_dict(self):
        return {
            'router_name': self.router_name,
            'device_ip': self.ip,
            'username': self.username,
            'password': self.password,
            'interface_list': [interface.open_dict() for interface in self.interface] if self.interface else [], 
            'ospf_dict': self.ospf_process.open_dict() if self.ospf_process else None
        }

    def __repr__(self):
        return f'{self.__class__.__name__}({self.router_name})'
    
# 表Interface
class Interface(Base):
    __tablename__ = 'interface'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey('router.id', ondelete='CASCADE'), nullable=False)
    interface_name = Column(String(64), nullable=False)
    ip = Column(String(64), nullable=False)
    mask = Column(String(64), nullable=False)

    # ----------定义relationshio属性----------
    # ----------Router----------
    router = relationship('Router', back_populates='interface', passive_deletes=True)

    def open_dict(self):
        return {
            'interface_name': self.interface_name,
            'ip': self.ip,
            'mask': self.mask
        }

    def __repr__(self):
        return f'{self.__class__.__name__}(Router: {self.router.router_name}) '\
               f'| Interface_name: {self.interface_name} ' \
               f'| IP: {self.ip} / {self.mask})' 

# 表OSPFProcess
class OSPFProcess(Base):
    __tablename__ = 'ospf_process'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey('router.id', ondelete='CASCADE'), nullable=False)
    processid = Column(Integer, nullable=False)
    routerid = Column(String(64), nullable=False)

    # ----------定义relationshio属性----------
    # ----------Router----------
    router = relationship('Router', back_populates='ospf_process', passive_deletes=True)
    # ----------Area----------
    area = relationship('Area', back_populates='ospf_process', passive_deletes=True)

    def open_dict(self):
        ospf_dict = { 'ospf_process_id': self.processid,
                      'router_id': self.routerid }
        network_list = []
        for area in self.area:
            for network in area.ospf_network:
                network_list.append({
                    'network': network.network,
                    'wildmask': network.wildmask,
                    'area': area.area_id
                })
        ospf_dict['network_list'] = network_list
        return ospf_dict              

    def __repr__(self):
        return f'{self.__class__.__name__}(Router: {self.router.router_name} ' \
               f'| Process: {self.processid})' 

# 表Area
class Area(Base):
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True)
    ospfprocess_id = Column(Integer, ForeignKey('ospf_process.id', ondelete='CASCADE'), nullable=False)
    area_id = Column(Integer, nullable=False)

    # ----------定义relationshio属性----------
    # ----------OSPF Process----------
    ospf_process = relationship('OSPFProcess', back_populates='area', passive_deletes=True)
    # ----------OSPF Network----------
    ospf_network = relationship('OSPFNetwork', back_populates='area', passive_deletes=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(Router: {self.ospf_prcess.router.router_name} ' \
               f'| Process: {self.ospf_process.processid} ' \
               f'| Area: {self.area_id})'

# 表OSPF Network
class OSPFNetwork(Base):
    __tablename__ = 'ospf_network'

    id = Column(Integer, primary_key=True)
    area_id = Column(Integer, ForeignKey('area.id', ondelete='CASCADE'), nullable=False)
    network = Column(String(64), nullable=False)
    wildmask = Column(String(64), nullable=False)

    # ----------定义relationshio属性----------
    # ----------Area----------
    area = relationship('Area', back_populates='ospf_network', passive_deletes=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(Router: {self.area.ospf_prcess.router.router_name} ' \
               f'| Process: {self.area.ospf_process.processid} ' \
               f'| Area: {self.area.area_id} ' \
               f'| Network: {self.network}/{self.wildmask})' 

# 表CPU Usage
class CPUUsage(Base):
    __tablename__ = 'cpu_usage'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey('router.id', ondelete='CASCADE'), nullable=False)
    cpu_usage_percent = Column(Integer, nullable=False)
    cpu_usage_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    # ----------定义relationshio属性----------
    # ----------Router----------
    router = relationship('Router', back_populates='cpu_usage', passive_deletes=True)

    def __repr__(self):
        return f'{self.__class__.__name__}(Router: {self.router.router_name} ' \
               f'| Datetime: {self.cpu_usage_datetime} ' \
               f'| Percent: {self.cpu_usage_percent})'

# 表Device Config
class DeviceConfig(Base):
    __tablename__ = 'device_config'

    id = Column(Integer, primary_key=True)
    router_id=Column(Integer, ForeignKey('router.id', ondelete='CASCADE'), nullable=False)
    device_config = Column(String(99999), nullable=False)
    config_md5 = Column(String(100), nullable=False)
    router = relationship('Router', back_populates='device_config', passive_deletes=True)
    record_time = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f'{self.__class__.__name__}(Device IP: {self.router.ip} ' \
               f'| Datetime: {self.record_time} ' \
               f'| Config MD5: {self.config_md5})'


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine, checkfirst=True)