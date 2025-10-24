from genie.testbed import load
from genie.utils.diff import Diff
import os
from genie.libs.conf.ospf import Ospf
from genie.libs.conf.ospf.areanetwork import AreaNetwork
from genie.libs.conf.vrf import Vrf
from genie.conf.base import Interface

import time, datetime, builtins

from pyats_write_table import write_ospf_status_db

# 当前项目目录的绝对路径
current_dir = os.path.dirname(os.path.realpath(__file__))

# 加载testbed数据
testbed = load(f'{current_dir}{os.sep}device_info.yaml')

# 提取设备c8Kv1
c8kv1 = testbed.devices['C8Kv1']

# 连接设备c8Kv1
c8kv1.connect(learn_hostname=True,
              log_stdout=False,
              ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')

# 当进行比较的两个内容中都拥有以下的值且不相同时则进行排除
exclude_list = ['(.*age.*)',
                '(.*checksum.*)',
                '(.*seq_num.*)',
                '(.*length.*)',
                '(.*hello_timer.*)',
                '(.*dead_timer.*)',
                '(.*area_scope_lsa_cksum_sum.*)']

# 提取设备c8Kv2
c8kv2 = testbed.devices['C8Kv2']

# 连接设备c8Kv1
c8kv2.connect(learn_hostname=True,
              log_stdout=False,
              ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')

# 默认全局VRF
vrf0= Vrf('default')

def print_with_time(*args, **kwargs):
    """自动给print输出加上时间戳"""
    ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    builtins.print(ts, *args, **kwargs)

# 覆盖默认print行为，附上时间戳
print = print_with_time


def build_c8kv2_config():
    """
    配置C8Kv2的Loopback1接口及OSPF
    """
    
    # 创建一个Loopback1接口
    intf = Interface(device=c8kv2, name='Loopback1')
    print("正在配置C8Kv2的Loopback1接口...")
    # 配置Loopback1接口的描述， IP， 掩码并使能
    intf.description = '< For Qytang NetDevOps>'
    intf.ipv4 = '11.1.1.1'
    intf.ipv4.netmask = '255.255.255.0'
    intf.shutdown = False

    # 产生接口配置
    intf.build_config()

    # 创建OSPF配置
    print("正在配置C8Kv2的OSPF...")
    ospf_obj = Ospf()
    # 定义要进行配置OSPF的设备、VRF和进程号
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].instance = '1'
    # 启用该 VRF 下的 OSPF 功能，相当于激活这个实例
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].enable = True
     # 设置 OSPF router-id
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].router_id = '11.1.1.1'

    # 宣告OSPF网络2.2.2.2/32
    an1 = AreaNetwork(device=c8kv2)
    an1.area_network= '2.2.2.2'
    an1.area_network_wildcard = '0.0.0.0'
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].area_attr['0'].add_areanetwork_key(an1)

    # 宣告OSPF网络61.128.1.0/24
    an2 = AreaNetwork(device=c8kv2)
    an2.area_network= '61.128.1.0'
    an2.area_network_wildcard = '0.0.0.255'
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].area_attr['0'].add_areanetwork_key(an2)

    # 宣告OSPF网络202.100.1.0/24
    an3 = AreaNetwork(device=c8kv2)
    an3.area_network= '202.100.1.0'
    an3.area_network_wildcard = '0.0.0.255'
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].area_attr['0'].add_areanetwork_key(an3)

    # 宣告OSPF网络11.1.1.0/24
    an4 = AreaNetwork(device=c8kv2)
    an4.area_network= '11.1.1.0'
    an4.area_network_wildcard = '0.0.0.255'
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].area_attr['0'].add_areanetwork_key(an4)

    # 把 ospf_obj这个OSPF配置对象添加到设备c8kv2的特性集中
    c8kv2.add_feature(ospf_obj)

    # 产生OSPF配置
    ospf_obj.build_config()

    # 等待10秒
    time.sleep(10)
    print("C8Kv2配置成功...")

def shutdown_c8kv2_loopback(timer):
    """
    在指定时间(分钟)后关闭C8Kv2的Loopback1接口

    参数:
        timer(int): 分钟
    """
    print(f'{timer}分钟后关闭C8Kv2的Loopback1接口')
    time.sleep(timer*60)

    intf_name = 'Loopback1'

    # 从设备中获取已存在接口对象
    print("正在关闭C8Kv2的Loopback1接口...")
    intf = c8kv2.interfaces.get(intf_name)
    # 关闭接口
    intf.shutdown = True
    intf.build_config()

    # 等待3秒
    time.sleep(3)
    # 查询接口状态
    try:
        intf_data = c8kv2.learn('interface').info
        if intf_name in intf_data:
            oper_status = intf_data[intf_name]['oper_status']
            enabled = intf_data[intf_name].get('enabled', None)
            print(f"接口{intf_name} 当前状态: oper_status={oper_status}, enabled={enabled}")
        else:
            print(f"未找到接口 {intf_name} 的状态信息。")
    except Exception as e:
        print(f"查询接口状态失败: {e}")


def del_c8kv2_ospf():
    """
    删除c8kv2上的所有OSPF配置
    """
    #创建OSPF实例
    ospf_obj = Ospf()
    # 定义要进行配置OSPF的设备、VRF和进程号
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].instance = '1'
    # 启用该 VRF 下的 OSPF 功能，相当于激活这个实例
    ospf_obj.device_attr[c8kv2].vrf_attr[vrf0].enable = True
    # 把 ospf_obj这个OSPF配置对象添加到设备c8kv2的特性集中
    c8kv2.add_feature(ospf_obj)
    
    # 删除配置
    ospf_obj.build_unconfig()

    # 等待10秒
    time.sleep(10)


if __name__ == '__main__':
    # 配置C8Kv2的Loopback1接口和OSPF
    build_c8kv2_config()

    # 5分钟后关闭C8Kv2的Loopback1接口使OSPF状态发生变化
    shutdown_c8kv2_loopback(5)