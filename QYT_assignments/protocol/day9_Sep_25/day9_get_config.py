#!/usr/bin/env python3
from sqlalchemy import all_
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os,sys, asyncio, threading, re
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

sys.path.append(str(project_root))

# 导入netmiko_show_cred模块
from day9_Sep_25.tools.netmiko_show_client import netmiko_show_cred
# 导入MD5值计算模块
from day9_Sep_25.tools.md5_gen import get_hash

async def async_netmiko_show(router_records):
    """
    异步采集多台设备的配置
    """
    # 协程任务列表
    tasks = []
    # 任务计数器
    task_no = 1

    for router in router_records:
        print(router.ip)        
        # 为netmiko_show_cred创建协程任务
        async def task_wrapper(task_id, router):
            print(f'------ID: {task_id} 开始获取路由器{router.ip}的配置------\n')
            device_config_raw = await asyncio.to_thread(
                netmiko_show_cred, 
                router.ip, 
                router.username, 
                router.password, 
                'show run')
            print(f'路由器{router.ip}配置获取成功\n')

            # 基于hostname关键字对device_config_raw进行切片
            # split_result[0]是show run结果中hostname之前的一段信息
            # split_result[1]是show run结果中hostname之后的一段信息
            split_result = re.split(r'\nhostname \S+\n', device_config_raw)
            # 删除原先完整的show run配置信息中hostname之前的部分
            run_config = device_config_raw.replace(split_result[0],'').strip()
            return {"ip": router.ip, "device_config": run_config, 'config_md5':get_hash(run_config)}
        # 把协程任务添加至任务列表
        tasks.append(task_wrapper(task_no, router))
        # 任务计数器递增
        task_no += 1
    
    # 执行协程任务列表中的所有任务
    return await asyncio.gather(*tasks, return_exceptions=True)



"""
asyncio.to_thread
Python 3.9 引入，用来简化 loop.run_in_executor。效果是一样的：把阻塞函数丢到线程池，避免卡住事件循环。

并发采集
每台设备的 show run 都是独立的阻塞 SSH 任务，丢到线程池后 asyncio 可以同时等待，达到“伪并发”的效果。

返回结果
我让 async_netmiko_show 返回一个字典（包含 task_id、ip、配置内容），便于后续保存到数据库或文件。
"""