#!/usr/bin/env python3.11
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def snmpv3_get(ip,
                    username,
                    auth_key,
                    priv_key,
                    oid,
                    auth_protocol=usmHMACSHAAuthProtocol,
                    priv_protocol=usmAesCfb128Protocol,
                    port=161):
    """
    向设备发送SNMPv3 GET请求并返回指定OID的值

    参数：
        ip(str): 设备的管理用IPv4地址
        username(str): SNMPv3用户名
        auth_key(str): SNMPv3认证密码
        priv_key(str): SNMPv3加密密钥
        oid(str): OID
        auth_protocol(var):SNMPv3认证算法，默认为SHA
        priv_protocol(var):SNMPv3加密算法, 默认为AES 128
        port(int): SNMP端口号
    返回：
        元组：包含OID和对应的值
    """
    # 创建SNMP引擎实例                
    snmp_engine = SnmpEngine()
    # 创建SNMPv3用户认证数据的实例
    user_data = UsmUserData(
        username,
        auth_key,
        priv_key,
        authProtocol=auth_protocol,
        privProtocol=priv_protocol
    )
    # 配置目的地址和端口号
    target = await UdpTransportTarget.create((ip, port))
    # 指定要查询的OID
    object_type = ObjectType(ObjectIdentity(oid))
    # 等待并获取SNMP GET的返回结果
    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        snmp_engine,
        user_data,
        target,
        ContextData(),
        object_type
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(f'{errorStatus} at {errorIndex and varBinds[int(errorIndex) -1 ][0] or "?"}')
    else:
        var_bind = varBinds[0]
        oid_id = var_bind[0]  # 获取OID
        oid_value = var_bind[1] # 获取OID对应的值
        if isinstance(oid_value, bytes):
            result_str = bytes.fromhex(oid_value[2:].decode('utf-8')).decode('utf-8', errors='ignore')
        else:
            result_str = str(oid_value)
        return oid_id.prettyPrint(), result_str

if __name__ == "__main__":
    # ip 地址与 snmp community 字符串
    ip_address = "10.10.1.101"
    username = "qytanguser"
    qytang_auth_key = 'Cisc0123'
    qytang_priv_key = 'Cisc0123'

    # cpmCPUTotal5sec
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key,
                                 "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7")))
    # cpmCPUMemoryUsed
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key,
                                 "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7")))
    # cpmCPUMemoryFree
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key,
                                 "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7")))