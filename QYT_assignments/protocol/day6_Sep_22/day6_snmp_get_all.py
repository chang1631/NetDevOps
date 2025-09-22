import asyncio
from pathlib import Path
import sys

parent_path = Path(__file__).parent
sys.path.insert(1, str(parent_path))
from day6_snmp_getbulk import snmpv3_getbulk

async def snmpv3_get_all_ifaces(devices_list, 
                         username, 
                         auth_key, 
                         priv_key, 
                         oids = {'if_name':'1.3.6.1.2.1.2.2.1.2',
                                'if_in_bytes': '1.3.6.1.2.1.2.2.1.10',
                                'if_out_bytes': '1.3.6.1.2.1.2.2.1.16',
                               }
                        ):
    """
    向多台设备发起发起SNMP请求并统一获取结果

    参数：
        devices_list(list): 设备的管理用IPv4地址列表
        username(str): SNMPv3用户名
        auth_key(str): SNMPv3认证密码
        priv_key(str): SNMPv3加密密钥
        oid(dict): OID字典
    返回：
        列表：包含了每台设备的管理IP地址及接口信息的字典
    """

    async def snmp_getbulk(ip_address):
        """
        单台设备上异步发起SNMP GETBULK请求

        返回一个列表包含了全部的snmp_getbulk返回的结果(列表)
        一个snmp_getbulk返回的结果(列表)中包含了多个OID和对应值的元组
        [
            [('1.3.6.1.2.1.2.2.1.2.1', 'GigabitEthernet1'), ('1.3.6.1.2.1.2.2.1.2.2', 'GigabitEthernet2'), ('1.3.6.1.2.1.2.2.1.2.3', 'GigabitEthernet3'), ('1.3.6.1.2.1.2.2.1.2.4', 'Null0')], 
            [('1.3.6.1.2.1.2.2.1.10.1', '1026732953'), ('1.3.6.1.2.1.2.2.1.10.2', '1203399798'), ('1.3.6.1.2.1.2.2.1.10.3', '20472781'), ('1.3.6.1.2.1.2.2.1.10.4', '0')], 
            [('1.3.6.1.2.1.2.2.1.16.1', '2289524794'), ('1.3.6.1.2.1.2.2.1.16.2', '514749152'), ('1.3.6.1.2.1.2.2.1.16.3', '0'), ('1.3.6.1.2.1.2.2.1.16.4', '0')]
        ]
        """
        results = await asyncio.gather(*[
        snmpv3_getbulk(ip_address, username, auth_key, priv_key, oid)
        for oid in oids.values()
    ])  
        try:
            # results是snmp_getbulk(ip_address)返回的一个列表，包含了所有GETBULK返回的结果
            # 每个GETBULK返回的结果是一个列表，其中每个元素是一个包含了OID和Value的元组
            raw_if_name_list = results[0]
            if_name_list = [raw_if_name[1] for raw_if_name in  raw_if_name_list]

            raw_in_bytes_list = results[1]
            in_bytes_list = [in_bytes[1] for in_bytes in raw_in_bytes_list]

            raw_out_bytes_list = results[2]
            out_bytes_list = [out_bytes[1] for out_bytes in raw_out_bytes_list]   

            interface_list = []
            for name, in_bytes, out_bytes in zip(if_name_list, in_bytes_list, out_bytes_list):
                interface_list.append({
                    'interface_name': name,
                    'in_bytes': in_bytes,
                    'out_bytes': out_bytes
                })
            # 返回一个包括了设备IP和接口信息列表的字典
            return{
                'device_ip':ip_address,
                'interface_list':interface_list
            }
        except Exception as e:
            print(f'SNMP GET执行失败：{str(e)}')
            return
    
    # 将所有需要执行的任务追加至一个列表
    tasks = [snmp_getbulk(ip) for ip in devices_list]

    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    # ip 地址与 snmp community 字符串
    devices = ["10.10.1.101", "10.10.1.102"]
    username = "qytanguser"
    qytang_auth_key = 'Cisc0123'
    qytang_priv_key = 'Cisc0123'

    from pprint import pprint
    results = asyncio.run(snmpv3_get_all_ifaces(devices, username, qytang_auth_key, qytang_priv_key))
    # pprint(results)
    """
        [{'device_ip': '10.10.1.101',
    'interface_list': [{'in_bytes': '883403420',
                        'interface_name': 'GigabitEthernet1',
                        'out_bytes': '2465712496'},
                        {'in_bytes': '1280647068',
                        'interface_name': 'GigabitEthernet2',
                        'out_bytes': '459630256'},
                        {'in_bytes': '33135645',
                        'interface_name': 'GigabitEthernet3',
                        'out_bytes': '0'},
                        {'in_bytes': '0',
                        'interface_name': 'Null0',
                        'out_bytes': '0'}]},
    {'device_ip': '10.10.1.102',
    'interface_list': [{'in_bytes': '1026326293',
                        'interface_name': 'GigabitEthernet1',
                        'out_bytes': '2289504858'},
                        {'in_bytes': '1203332411',
                        'interface_name': 'GigabitEthernet2',
                        'out_bytes': '514747556'},
                        {'in_bytes': '20428708',
                        'interface_name': 'GigabitEthernet3',
                        'out_bytes': '0'},
                        {'in_bytes': '0',
                        'interface_name': 'Null0',
                        'out_bytes': '0'}]}]
    """