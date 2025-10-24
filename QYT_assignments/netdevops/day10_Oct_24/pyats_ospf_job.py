#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from genie.utils.diff import Diff
import json

from pyats_create_table import engine, PyatsOSPF
from pyats_tools import c8kv1, c8kv2, exclude_list, print_with_time
from pyats_write_table import write_ospf_status_db
from send_warning_mail import send_ospf_status_update_mail
from smtp_info import smtp_dict

Session = sessionmaker(bind=engine)
session = Session()

# 覆盖默认print行为，附上时间戳
print = print_with_time

def normalize_keys(data):
    """
    递归将所有 dict 的键转换为字符串

    参数:
        data(dict): OSPF状态数据
    返回：
        键被转换成字符串后的字典
    """
    if isinstance(data, dict):
        return {str(k): normalize_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_keys(i) for i in data]
    else:
        return data

def ospf_compare_task(devices_list, smtp_dict):
    """
    对比设备当前OSPF状态与对应的数据库中最近一次的OSPF状态;如果有差异则发送告警邮件.
    最终将获取到的OSPF状态信息写入数据库中

    参数:
        devices_list(list): pyATS设备列表
        smtp_dict(dict): SMTP账户信息
    """ 
    for device in devices_list:
        ospf_data_dict = {}
        # 提取结果中的设备名称
        device_name= device.name

        # 提取设备当前的OSPF状态
        # 这里有一个坑，获取 OSPF 学习结果时，to_dict() 生成的结构中包含混合类型的键
        # 例如{'lsa_types': {1: 和'topologies': {0：中的数字是整数
        # 而当该数据存入数据库并重新读取时，JSON 会把所有键都转为字符串类型，因为 JSON 标准不支持非字符串键
        # 这会造成即使没有修改过配置，Diff也会发现差异的原因
        # 所以在写入数据库前统一键类型，将其转换为字符串
        ospf_data_latest =  normalize_keys(device.learn('ospf').to_dict())
        
        # 通过设备名称、管理IP地址、OSPF状态和OSPF路由表信息构建字典ospf_data_dict
        ospf_data_dict['device_name'] = device_name
        ospf_data_dict['device_ip'] = str(device.connections['cli'].ip)
        ospf_data_dict['ospf_status'] = ospf_data_latest
        # 尝试获取到OSPF路由表
        ospf_rt = {}
        try:
            # 如果获取成功则转换成字典并追加至字典ospf_data_dict
            ospf_rt.update(device.parse('show ip route ospf'))
            # device.parse('show ip route ospf') 是<class 'genie.conf.base.utils.QDict'>对象，不是字典需要进行转换
            ospf_data_dict['route_table_status'] = json.loads(json.dumps(ospf_rt))
        except:
            ospf_data_dict['route_table_status'] = ospf_rt
        
        
        # 根据设备名称在数据库中找到该路由器记录的实例
        router = session.query(PyatsOSPF).filter(PyatsOSPF.device_name == device_name).first()
        # 如果有该设备的记录
        if router:
            # 查询该router的最近一次的记录
            ospf_record_prev = session.query(PyatsOSPF).filter(PyatsOSPF.device_name == device_name).order_by(PyatsOSPF.record_datetime.desc()).first()

            # 如果该路由器拥有记录则提取相关OSPF状态信息
            if ospf_record_prev:
                ospf_data_prev = ospf_record_prev.ospf_status

                # 将当前OSPF状态信息与数据库中最近一次的OSPF状态信息进行比较
                diff = Diff(ospf_data_prev, ospf_data_latest, exclude=exclude_list)
                diff.findDiff()
                # 如果当前OSPF状态信息与最近一次备份的OSPF状态信息不一致则发送告警邮件
                if diff.diffs:
                    main_body = str(diff)
                    send_ospf_status_update_mail(device_name, main_body,**smtp_dict)
                else:
                    print(f'{device_name}-OSPF状态未发生变化')
        
        # 将获取的路由器OSPF等相关信息写入数据库
        write_ospf_status_db(ospf_data_dict)


if __name__ == '__main__':
    devices_list = [c8kv1, c8kv2]
    ospf_compare_task(devices_list, smtp_dict)