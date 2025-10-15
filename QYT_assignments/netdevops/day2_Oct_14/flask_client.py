#!/usr/bin/env python3
import requests, base64, os, sys
from pathlib import Path
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

server_ip = '10.10.1.200'
server_port = '8080'
base_url = fr'http://{server_ip}:{server_port}/'
exec_cmd_url = base_url + 'cmd'         # 执行命令的URL
upload_url = base_url + 'upload'        # 上传文件的URL
download_url = base_url + 'download'    # 下载文件的URL 

# 文件的下载路径
download_file_dir = f'{parrent_dir}{os.sep}download_img/'

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

def json_rpc_client_upload(filename):
    '''
    向服务器发送POST请求并上传指定的文件

    参数：
        filename(str): 文件名
    返回：
        服务器的响应结果(str)
    '''
    # 补全文件文件的完整路径
    img_path = f'{parrent_dir}{os.sep}{filename}'
    # 如果文件文件名不为空则通过Base64对文件文件进行编码
    if filename:
        try:
            # 以二进制形式读取文件
            with open(img_path, 'rb') as f:
                img_bytes = f.read()    
            img_base64 = base64.b64encode(img_bytes).decode()
            # 将文件名信息和文件的Base64编码信息存储在字典中
            img_dict = {'upload_filename':filename,'file_bit':img_base64}
            post_req = requests.post(upload_url, json=img_dict)
            post_req.raise_for_status()
            try: 
                upload_result = post_req.json()
                # 如果JSON信息中有'message'键，说明上传成功
                if 'message' in upload_result:
                    return upload_result
                else:
                    return base64_to_str(upload_result['error']).strip()
            except requests.exceptions.HTTPError as e:
                return f'HTTP错误:\n\t错误详细信息{e}\n\t状态码:{e.response.status_code}'
            except Exception as e:
                return f'服务器连接异常:{str(e)}'
        # 处理未找到本地文件的异常情况
        except Exception as e:
            # 字典中只包含文件名信息
            img_dict = {'upload_filename':filename}
            post_req = requests.post(upload_url, json=img_dict)
            upload_result = post_req.json()
            # 返回错误消息
            return upload_result['error']
    # 没有传入文件文件名则直接将{'upload_filename':filename}作为JSON数据向服务器发送POST请求
    # 仅用于测试服务器处理异常JSON数据
    else:
        post_req = requests.post(upload_url, json='')
        upload_result = post_req.json()
        return upload_result['error']

def json_rpc_client_download(filename):
    '''
    向服务器发送POST请求并下载指定的文件

    参数：
        filename(str): 文件名
    返回：
        服务器的响应结果(str)
    '''
    img_dict = {'download_filename':filename}
    try:
        post_req = requests.post(download_url, json=img_dict)
        post_req.raise_for_status()
        try :
            download_result = post_req.json()
            # 如果JSON信息中有'message'键，说明下载成功
            if 'message' in download_result:
                # 获取下载成功的提示信息
                message = download_result['message']
                # 获取文件的Base64编码
                img_base64 = download_result['img_base64']
                # 在指定的下载文件路径中新建文件并以filename命令
                fp = open(download_file_dir + filename, 'wb')
                # 对file_bit字节对象进行base64解码，得到原始的二进制数据并写入文件
                fp.write(base64.b64decode(img_base64.encode()))
                fp.close()
                print(message)
            # 如果JSON信息中有'no_file_error'键，说明服务器端没有找到文件，打印错误信息
            elif 'no_file_error' in download_result:
                file_not_found_message = download_result['no_file_error']
                print(file_not_found_message)
            else:
                print(download_result['error'])
        except Exception as e:
            print(f'获取数据失败:{str(e)}')
    except requests.exceptions.HTTPError as e:
        print(f'HTTP错误:\n\t错误详细信息{e}\n\t状态码:{e.response.status_code}')
    except Exception as e:
        print(f'服务器连接异常:{str(e)}')


if __name__ == '__main__':
    exec_cmd = {'cmd':'ifconfig'}
    print(f'=====测试1 {exec_cmd_url}  方法:POST  JSON数据:{exec_cmd}=====')
    print(json_rpc_client_exec_cmd(exec_cmd))

    exec_cmd = {'cmd':'pwd1'}
    print(f'\n=====测试2 {exec_cmd_url}  方法:POST  JSON数据:{exec_cmd}=====')
    print(json_rpc_client_exec_cmd(exec_cmd))

    exec_cmd = {'cmd1':'pwd'}
    print(f'\n=====测试3 {exec_cmd_url}  方法:POST  JSON数据:{exec_cmd}=====')
    print(json_rpc_client_exec_cmd(exec_cmd))

    image_file_name = 'upload.jpg'
    print(f'\n=====测试4 {upload_url}  方法:POST  文件名:{image_file_name}=====')
    print(json_rpc_client_upload(image_file_name))

    image_file_name = 'download.png'
    print(f'\n=====测试5 {download_url}  方法:POST  文件名:{image_file_name}=====')
    json_rpc_client_download(image_file_name)

    image_file_name = 'download_bad.png'
    print(f'\n=====测试6 {download_url}  方法:POST  文件名:{image_file_name}=====')
    json_rpc_client_download(image_file_name)

    print('\n【其他异常测试】')
    exec_cmd = ''
    print(f'\n=====测试 {exec_cmd_url}  方法:POST  JSON数据:{exec_cmd}=====')
    print(json_rpc_client_exec_cmd(exec_cmd))

    image_file_name = 'upload_bad.jpg'
    print(f'\n=====测试{upload_url}  方法:POST  文件名:{image_file_name}=====')
    print(json_rpc_client_upload(image_file_name))

    image_file_name = ''
    print(f'\n=====测试{upload_url}  方法:POST  文件名:{image_file_name}=====')
    print(json_rpc_client_upload(image_file_name))

    print(f'\n=====测试{download_url}  方法:POST  文件名:{image_file_name}=====')
    json_rpc_client_download(image_file_name)