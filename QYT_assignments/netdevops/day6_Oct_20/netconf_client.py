#!/usr/bin/env python3

from ncclient import manager
from ncclient.operations import RPCError
import lxml.etree as et

def netconfig_request(ip, username, password, payload_xml, port='830'):
    """
    使用ncclient向设备发起自定义NETCONF RPC请求

    参数：
        ip(str): 设备的管理IPv4地址
        username(str): 用户名
        password(str): 密码
        payload_xml(str): XML字符串
        port(str): 端口号
    输出：
        设备返回的XML响应内容(转换为可读字符串)
    """
    # 与设备建立SSH连接并启动NETCONF子系统
    with manager.connect(host=ip,
                         port=port,
                         username=username,
                         password=password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'csr'}) as mg:
        
        try:
            # 发送自定义的XML RPC请求
            response = mg.dispatch(et.fromstring(payload_xml))
            # 将响应的数据转换为XML结构树
            data = et.fromstring(response._raw.encode())
        except RPCError as e:
            data = e._raw
        
        # 将data转换为Python字符串
        return et.tostring(data, encoding = 'unicode', pretty_print=True)