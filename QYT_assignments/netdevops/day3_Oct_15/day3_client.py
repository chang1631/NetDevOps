#!/usr/bin/env python3.11
import requests, base64

server_url = "fastapi.netdevops.com" 
base_url = f"https://{server_url}/"
exec_cmd_url = base_url + 'cmd'         # 执行命令的URL

def base64_to_str(base64str):
    '''
    对Base64编码格式的字符串进行解码

    参数：
        base64str(str): Base64格式的字符串
    返回：
        解码后的普通字符串
    '''
    return base64.b64decode(base64str).decode()

def json_rpc_client_exec_cmd(cmd_dict):
    '''
    向服务器发送POST请求和指定的JSON数据执行远端服务器的CMD命令

    参数:
        cmd_dict(dict): 向服务器发送的JSON数据
    返回：
        服务器的响应结果(str)
    '''
    try:
        # 向服务器发起POST请求并附上数据
        post_req = requests.post(exec_cmd_url, json=cmd_dict)
        post_req.raise_for_status()
        # 尝试提取服务器返回的JSON数据
        try: 
            cmd_result = post_req.json()
            # 如果返回的JSON信息中有'cmd'键，说明命令执行成功
            if 'cmd' in cmd_result:
                # 将结果通过Base64进行解码
                return base64_to_str(cmd_result['cmd_result'])
            # 否则将错误信息通过Base64进行解码并返回
            else:
                return base64_to_str(cmd_result['error']).strip()
        # 处理返回数据的异常情况
        except Exception as e:
            return f'获取数据失败:{str(e)}'
    # 处理HTTP状态码异常
    except requests.exceptions.HTTPError as e:
        return f'HTTP错误:\n\t错误详细信息{e}\n\t状态码:{e.response.status_code}'
    # 处理服务器连接异常
    except Exception as e:
        return f'服务器连接异常:{str(e)}'

if __name__ == '__main__':
    exec_cmd = {"cmd": "ifconfig"}
    print(f'\n=====测试1 {exec_cmd_url}  方法:POST  JSON数据:{exec_cmd}=====')
    print(json_rpc_client_exec_cmd(exec_cmd))

    exec_cmd = {"cmd":'ipconfig'}
    print(f'\n=====测试2 {exec_cmd_url}  方法:POST  JSON数据:{exec_cmd}=====')
    print(json_rpc_client_exec_cmd(exec_cmd))