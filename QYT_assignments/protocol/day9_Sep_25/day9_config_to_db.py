#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os,sys, asyncio, threading
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

sys.path.append(str(project_root))

# 导入数据库的model和engine
from day7_Sep_23.day7_1_psql_createdb import DeviceConfig, Router, engine

Session = sessionmaker(bind=engine)
session = Session()

def write_config_to_db(result_list):
    """
    将设备的配置信息及对应的MD5值写入数据库

    参数：
        result_list(list): Netmiko获取多台设备的配置信息
    """
    for result in result_list:
        # 提取结果中的设备IP地址
        device_ip = result['ip']
        # 基于设备IP地址筛选出对应的路由器记录实例
        router = session.query(Router).filter(Router.ip == device_ip).one()
        # 初始化字典用于后续为表device_config添加记录
        config_dict = {'router': router,
                       'device_config': result['device_config'],
                       'config_md5': result['config_md5']
                        }
        # 将配置信息和MD5值添加到字典 config_dict
        device_config = DeviceConfig(**config_dict)

        # 添加记录并提交
        session.add(device_config)
        session.commit()