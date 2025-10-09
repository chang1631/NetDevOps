#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from pprint import pprint
from jinja2 import Template
import os, sys, asyncio, threading
parrent_dir = Path(__file__).parent
from day7_1_psql_createdb import Router, engine
# 导入Netmiko设备配置模块
from tools.ssh_client_netmiko import netmiko_config_cred

# jinja2模板路径
jinja2_temp_dir = f'{parrent_dir}{os.sep}config_template{os.sep}'

# 加载jinja2 Cisco接口配置模板
with open(jinja2_temp_dir + 'cisco_ios_interface.jinja2') as tempf:
    interface_config_template = Template(tempf.read())

# 加载jinja2 Cisco OSPF配置模板
with open(jinja2_temp_dir + 'cisco_ios_ospf.jinja2') as tempf:
    ospf_config_template = Template(tempf.read())

# 创建异步事件池
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 为Netmiko定义一个携程函数
async def async_netmiko(task_id, ip, username, password, cmds_list):
    print(f'ID: {task_id} Started')
    print(os.getpid(), threading.current_thread().ident)
    result = await loop.run_in_executor(None, netmiko_config_cred, ip, username, password, cmds_list)
    print(f'ID: {task_id} Stopped')
    return result

Session = sessionmaker(bind=engine)
session = Session()

# 任务计数器
task_no = 1

# 协程任务列表
tasks = []

# 查询所有路由器的记录
all_routers = session.query(Router).all()

for router in all_routers:
    final_config_cmds_list = []
    # 提取设备IP
    device_ip = router.ip
    print(device_ip)

    # 提取设备SSH账户
    login_username = router.username
    login_password = router.password
    # 打开router记录实例的字典
    router_dict = router.open_dict()
    # pprint(router_dict)

    # 将接口数据放入接口配置模板进行填充
    interface_config_result = interface_config_template.render(router_dict=router_dict)
    # 将接口模板模板产生的配置通过split进行切分并添加至列表final_config_cmds_list
    final_config_cmds_list.extend(interface_config_result.split('\n'))

    # 将OSPF配置数据放入OSPF配置模板进行填充
    ospf_config_result = ospf_config_template.render(router_dict=router_dict)
    # 将OSPF模板产生的配置通过split进行切分并添加至列表final_config_cmds_list
    final_config_cmds_list.extend(ospf_config_result.split('\n'))

    # 创建协程任务
    task = loop.create_task(async_netmiko(task_no, device_ip, login_username, login_password, final_config_cmds_list))
    # 把协程任务添加至任务列表
    tasks.append(task)
    # 任务计数器递增
    task_no += 1

# 执行协程任务列表中的所有任务
loop.run_until_complete(asyncio.wait(tasks))