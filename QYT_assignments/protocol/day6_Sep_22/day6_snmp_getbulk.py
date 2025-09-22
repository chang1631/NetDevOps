#!/usr/bin/env python3.11
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.proto.secmod.eso import priv

async def snmpv3_getbulk(ip, username, auth_key, priv_key, oid, count=25, auth_protocol=usmHMACSHAAuthProtocol,
                         priv_protocol=usmAesCfb128Protocol, port=161):
      """
      批量获取多个OID信息
      
      返回：
          列表：包含OID和对应值的元组
      """     
      iterator = bulk_cmd(
            SnmpEngine(),
            UsmUserData(
                username,
                auth_key,
                priv_key,
                authProtocol=auth_protocol,
                privProtocol=priv_protocol
            ),
            await UdpTransportTarget.create((ip, port)),
            ContextData(),
            0, count,
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=True
      )

      error_indication, error_status, error_index, var_binds = await iterator

      if error_indication:
        print(f'读取错误！！！\n{error_indication}')
      elif error_status:
        print(f'读取错误！！！\n{error_status} at {error_index and var_binds[int(error_index) -1][0] or "?"}')
      else:
        result = []
        for var_bind_table_row in var_binds:
            get_oid = str(var_bind_table_row[0])
            get_value = str(var_bind_table_row[1])
            if oid not in get_oid:
                break
            result.append((get_oid, get_value))
        return result

if __name__ == "__main__":
    from pprint import pprint
    ip_address = "10.10.1.101"
    username = "qytanguser"
    qytang_auth_key = 'Cisc0123'
    qytang_priv_key = 'Cisc0123'

    raw_name_list = asyncio.run(snmpv3_getbulk(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.2.2.1.2", port=161))
    pprint(raw_name_list)
    #[('1.3.6.1.2.1.2.2.1.2.1', 'GigabitEthernet1'),('1.3.6.1.2.1.2.2.1.2.2', 'GigabitEthernet2'),('1.3.6.1.2.1.2.2.1.2.3', 'GigabitEthernet3'),('1.3.6.1.2.1.2.2.1.2.4', 'Null0')]


    # # 获取接口名称
    # raw_name_list = asyncio.run(snmpv3_getbulk(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.2.2.1.2", port=161))
    # if_name_list = [raw_if_name[1] for raw_if_name in raw_name_list]

    # # 获取进接口字节数
    # raw_in_bytes_list = asyncio.run(snmpv3_getbulk(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.2.2.1.10", port=161))
    # if_in_bytes_list = [raw_in_bytes[1] for raw_in_bytes in raw_in_bytes_list]

    # # 获取出接口字节数
    # raw_out_bytes_list = asyncio.run(snmpv3_getbulk(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.2.2.1.16", port=161))
    # if_out_bytes_list = [raw_out_bytes[1] for raw_out_bytes in raw_out_bytes_list]

    # interface_list = []
    # for name, in_bytes, out_bytes in zip(if_name_list, if_in_bytes_list, if_out_bytes_list):
    #     interface_list.append({
    #         'interface_name': name,
    #         'in_bytes': in_bytes,
    #         'out_bytes': out_bytes
    #     })

    
    # pprint(interface_list)
    

