#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os,sys, asyncio
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

sys.path.insert(1,str(project_root))

# 导入数据库表model和engine
from day7_Sep_23.day7_1_psql_createdb import Router, engine
# 导入获取配置模块
from day9_Sep_25.day9_get_config import async_netmiko_show
# 导入配置比对模块
from day9_Sep_25.day9_compare_conf import compare_config_warning
# 导入数据库写入模块
from day9_Sep_25.day9_config_to_db import write_config_to_db

def main(router_table_records, smtp_dict):
    """
    主程序入口，获取当前路由器配置，与数据库中最近一次的配置作比对；
    如果配置发生改变则发送告警邮件；
    将配置相关数据写入数据库；

    参数：
        router_table_records(obj): 表Router的记录实例
        smtp_dict(dict): SMTP相关参数

    """
    # 查询所有路由器的记录
    result_list = asyncio.run(async_netmiko_show(router_table_records))

    # 比对配置
    compare_config_warning(result_list, smtp_dict)
    
    # 将新获取的配置信息及对应的MD5值写入数据库
    write_config_to_db(result_list)

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()

    # 获取表router中全部路由器的记录
    routers = session.query(Router).all()

    # 定义SMTP参数
    smtp_dict = {'mailserver': os.environ.get('SMTPSERVER'),
                'username': os.environ.get('SMTPUSER'), 
                'password': os.environ.get('SMTPPASS'), 
                'from_mail': os.environ.get('SMTPUSER'), 
                'to_mail': '3882456661@qq.com'   
                }  
                
    # 执行主程序
    main(routers,smtp_dict)