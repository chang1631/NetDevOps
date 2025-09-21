import asyncio
from pathlib import Path
import sys

parent_path = Path(__file__).parent
sys.path.insert(1, str(parent_path))
from day4_snmp_get import snmpv3_get

async def snmpv3_get_all(devices_list, 
                         username, 
                         auth_key, 
                         priv_key, 
                         oids = {'cpu_usage':'1.3.6.1.4.1.9.9.109.1.1.1.1.6.7',
                                'mem_use': '1.3.6.1.4.1.9.9.109.1.1.1.1.12.7',
                                'mem_free': '1.3.6.1.4.1.9.9.109.1.1.1.1.13.7',
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
        列表：包含了每台设备返回的OID和对应值的字典
    """

    async def snmp_get(ip_address):
        """
        单台设备上异步发起SNMP GET请求
        """
        results = await asyncio.gather(*[
        snmpv3_get(ip_address, username, auth_key, priv_key, oid)
        for oid in oids.values()
    ])

        try:
            # 提取SNMP GET的结果
            cpu_usage = int(results[0][1])
            mem_use = int(results[1][1])
            mem_free = int(results[2][1])

            return{
                'device_ip':ip_address,
                'cpu_usage_percent':cpu_usage,
                'mem_use':mem_use,
                'mem_free':mem_free
            }
        except Exception as e:
            print(f'SNMP GET执行失败：{str(e)}')
            return
    
    # 将所有需要执行的任务追加至一个列表
    tasks = [snmp_get(ip) for ip in devices_list]

    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    # ip 地址与 snmp community 字符串
    devices = ["10.10.1.101", "10.10.1.102"]
    username = "qytanguser"
    qytang_auth_key = 'Cisc0123'
    qytang_priv_key = 'Cisc0123'

    results = asyncio.run(snmpv3_get_all(devices, username, qytang_auth_key, qytang_priv_key))
    print(results)




"""
👍 你的理解已经非常到位了，我帮你稍微打磨一下表述，让逻辑更清晰：

---

这段代码的执行流程可以这样理解：

1. **`snmpv3_get_all` 入口函数**

   * 接收设备列表 `devices_list`，以及用户凭证和 OIDs。
   * 在函数内部定义了一个 **异步子函数 `snmp_get`**，专门处理单台设备。

2. **单台设备：`snmp_get(ip_address)`**

   * 利用 `asyncio.gather` 并发向该设备发起多个 SNMP GET 请求（对应多个 OID）。
   * 等到这台设备的所有 OID 都返回结果后，提取出 CPU、内存等指标，打包成字典返回。
   * 👉 相当于：对单个设备的 **多个 OID 查询并发执行**，不需要一个个排队。

3. **多台设备：`snmpv3_get_all(devices_list, ...)`**

   * 创建一个任务列表：`tasks = [snmp_get(ip) for ip in devices_list]`
   * 再次用 `asyncio.gather`，并发运行这些单设备任务。
   * 👉 相当于：对 **多台设备同时** 做 SNMP 查询，每台设备内部又是 OID 并发。

4. **结果收集**

   * 外层 `gather` 会等待所有设备任务完成。
   * 返回值是一个列表，里面每个元素是某台设备的指标字典。
   * 谁先完成不重要，最终结果会按照任务列表的顺序（即 `devices_list` 的顺序）返回。

---

✅ 总结成一句话：

* **内层 `gather`**：并发获取同一台设备的多个 OID。
* **外层 `gather`**：并发获取多台设备的数据。
* 最终形成「多台设备、多 OID」的全量结果。

---

要不要我帮你改写一下，让返回结果结构更直观，比如变成这样：

```python
[
  {
    "device_ip": "192.168.1.1",
    "cpu_usage_percent": 12,
    "mem_use": 3456,
    "mem_free": 7890
  },
  {
    "device_ip": "192.168.1.2",
    "cpu_usage_percent": 34,
    "mem_use": 5678,
    "mem_free": 1234
  }
]
```

这样你直接就能用 JSON 或 Pandas 处理分析。要不要我帮你优化返回结构？

"""