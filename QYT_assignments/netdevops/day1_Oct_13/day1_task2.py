#!/usr/bin/env python3
from requests.auth import HTTPBasicAuth
import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router_mgmt_ip = '10.10.1.101'
username = 'admin'
password = 'Cisc0123'

def get_interfaces_info(mgmt_ip, username, password):
    '''
    通过路由器的REST API获取接口信息

    参数：
        mgmt_ip(str): 路由器的管理IP地址
        username(str): 路由器管理员用户名
        password(str): 路由器管理员密码
    返回：
        HTTP响应的内容(str)
    '''
    url = f'https://{mgmt_ip}/level/15/exec/-/show/ip/interface/brief/CR'
    try:
        resp = requests.get(url, 
                            auth=HTTPBasicAuth(username, password),
                            verify=False)
        # 如果HTTP状态码为200则返回响应内容
        if resp.status_code == 200:
            return resp.text
        else:
            print(f'HTTP响应异常{str(resp.status_code)}')
            return None
    except Exception as e:
        print(f'获取接口信息失败:{str(e)}')
        return None

if __name__ == '__main__':
    router_response = get_interfaces_info(router_mgmt_ip, username, password)
    print(router_response)