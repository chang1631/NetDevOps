#!/usr/bin/env python3

from requests.auth import HTTPBasicAuth
import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ASA管理员账户
asa_username = 'admin'
asa_password = 'ciscoasa'

# ASA的URL
asa_server = 'https://10.10.1.110'

# API Token Path
api_token_path = '/api/tokenservices'
# Syslogserver Path
syslogserver_path = '/api/logging/syslogserver'

# 获取API Token的完整URL
api_token_url = asa_server + api_token_path
# 配置Syslog服务器的完整URL
syslogserver_url = asa_server + syslogserver_path

# 初始化HTTP Request Headers
request_headers = {"Content-Type": "application/json", "Accept": "application/json"}

def get_token():
    """
    获取ASA的API Token

    返回：
        API Token字符串
    """
    # 发送POST请求获取 API Token
    try:
        resp =  requests.post(api_token_url,
                              headers=request_headers,
                              auth=HTTPBasicAuth(asa_username,asa_password),
                              verify=False)
        # 提取Response Headers中的'X-Auth-Token'字段
        return resp.headers['X-Auth-Token']
    # 处理异常
    except Exception as e:
        print(f'Token获取失败:{str(e)}')
        return

def config_syslog(ifname, syslog_server_ip, token):
    """
    通过ASA REST API配置Syslog服务器

    参数:
        ifname(str): ASA连接Syslog日志服务器的接口名称(nameif)
        syslog_server_ip(str): Syslog日志服务器的IPv4地址
        token(str): API Token
    返回：
        HTTP响应状态码
    """
    # 拷贝request_headers字典并赋值给新的变量request_headers_with_token
    request_headers_with_token = request_headers.copy()
    # 将token添加至字典request_headers_with_token形成带有token的HTTP Request Headers
    request_headers_with_token["X-Auth-Token"]=token
    # 构建POST请求数据
    post_data = {"ip": {
                    "kind": "IPv4Address",
                    "value": syslog_server_ip
                    },
                    "interface": {
                        "kind": "objectRef#Interface",
                        "name": ifname
                    },
                    "port": 1040,
                    "emblemEnabled": False,
                    "secureEnabled": False,
                    "protocol": "TCP"}
    # 发送POST请求以配置Syslog服务器
    try:
        resp =  requests.post(syslogserver_url,
                              headers=request_headers_with_token,
                              json = post_data,
                              verify=False)
        # 抛出异常HTTP响应异常
        resp.raise_for_status()
        print('Syslog服务器配置成功！')
        return resp.status_code
    # 处理异常HTTP状态码
    except requests.exceptions.HTTPError as e:
        return f'Syslog服务器配置失败:\n\t错误详细信息{e}\n\t状态码:{e.response.status_code}'
    # 处理其他异常
    except Exception as e:
        print(f'POST请求失败:{str(e)}')



if __name__ == '__main__':
    # 获取API Token
    api_token = get_token()
    # 接口名称
    ifname = "syslog_g0/2"
    # Syslog服务器的IP地址
    syslog_server_ip = "30.1.1.200"
    # 发起POST请求配置Syslog服务器
    post_resp = config_syslog(ifname, syslog_server_ip, api_token)
    print(post_resp)