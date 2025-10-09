#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os,sys, asyncio, re
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

sys.path.append(str(project_root))

# 导入数据库的model和engine
from day7_Sep_23.day7_1_psql_createdb import DeviceConfig, Router, engine
# 导入告警邮件发送模块
from day9_Sep_25.day9_send_config_mail import send_config_mail
# 导入diff_txt模块
from day9_Sep_25.tools.diff_config import diff_txt

Session = sessionmaker(bind=engine)
session = Session()

def compare_config_warning(result_list, smtp_dict):
    """
    比对当前配置的MD5值和上一次配置的MD5

    参数：
        result_list(list): async_netmiko_show函数的返回结果
    """
    for result in result_list:
        # 提取结果中的设备IP地址
        device_ip= result['ip']
        # 提取结果中的设备配置
        current_config = result['device_config']
        # 提取结果中的MD5值
        current_md5 = result['config_md5']
        router = session.query(Router).filter(Router.ip == device_ip).first()

        if router:
            # 查询该router的最近一次的DeviceConfig记录
            latest_config_record = session.query(DeviceConfig).filter(
                DeviceConfig.router_id == router.id
            ).order_by(DeviceConfig.record_time.desc()).first()

            # 如果该路由器拥有记录则提取相关信息并与当前配置进行比对
            if latest_config_record:
                # 获取上一次的配置内容和对应的MD5值
                last_config = latest_config_record.device_config
                last_md5 = latest_config_record.config_md5

                # 如果新获取配置的MD5值与上一次备份配置的MD5值不相同则发送告警邮件
                if current_md5 != last_md5:
                    print(f'设备 {device_ip}的配置发生变更！！！')
                    # 将配置之间的比对结果添加至邮件的主体中
                    comp_res=diff_txt(last_config, current_config)
                    send_config_mail(device_ip,
                                     comp_res,
                                     **smtp_dict)
                else:
                    print(f'设备 {device_ip}的配置未发生改变\n')