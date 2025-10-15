#!/usr/bin/env python3
from flask import Flask, request
from pathlib import Path
import os, sys, subprocess, base64
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

# 创建一个Flask应用实例
node = Flask(__name__)

# 输出Debug消息
node.debug = True

# 文件的上传路径   
server_file_dir = f'{parrent_dir}{os.sep}upload_img{os.sep}'

def system_cmd(cmd_command):
    '''
    根据传入的cmd字符串执行Linux命令

    参数：
        cmd_command(str): 命令字符串
    返回：
        包含标准输出和标准错误的元组
    '''
    cmd_list = cmd_command.split(' ')
    process = subprocess.Popen(cmd_list,
                              shell=True, 
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True 
    )
    # 与子进程交互，发送输入并获取输出
    stdout, stderr = process.communicate()
    # 返回标准输出和标准错误
    return stdout, stderr

# 执行命令的路由'cmd', 限制只能使用POST请求
@node.route('/cmd', methods=['POST'])
def cmd():
    client_post_data = request.json
    if client_post_data:
        # 提取'cmd'的值，如果不是JSON格式的数据则返回'json format error'的报错
        try:
            cmd_command = client_post_data.get('cmd')
        except AttributeError:
            return {'error': base64.b64encode('json format error'.encode()).decode()}
        if cmd_command:
            # 调用system_cmd函数执行命令
            cmd_result = system_cmd(cmd_command)
            # 如果cmd_result[1]有返回内容，表示命令执行错误
            if cmd_result[1]:
                # 将命令执行的错误结果转换成字节对象，再用Base64进行编码转换到安全的输出
                return {'error': base64.b64encode(cmd_result[1].encode()).decode()}
            # 如果cmd_result[1]没有返回内容，表示命令执行成功
            else:
                # 将命令执行的结果转换成字节对象，再用Base64进行编码转换到安全的输出
                return {'cmd': cmd_command, 'cmd_result': base64.b64encode(cmd_result[0].encode()).decode()}
        # 如果json数据中没有键'cmd'则报错
        else:
             return {'error': base64.b64encode('no cmd in json'.encode()).decode()}
    # 没有上传json数据则报错
    else:
        return {'error': base64.b64encode('no json data'.encode()).decode()}

# 上传文件的路由'upload', 限制只能使用POST请求
@node.route('/upload', methods=['POST'])
def upload():
    client_post_data = request.json
    # 如果有json数据
    if client_post_data:
        # 提取键'upload_filename'和'file_bit'对应的值，如果JSON格式错误，返回'json format error'的报错
        try:
            upload_filename = client_post_data.get('upload_filename')
            file_bit = client_post_data.get('file_bit')
        except AttributeError:
            return {'error': base64.b64encode('json format error'.encode()).decode()}
        # 如果'upload_filename'和'file_bit'的值同时存在
        if upload_filename and file_bit:
            # 在指定的上传文件路径中新建文件并以filename命令
            fp = open(server_file_dir + upload_filename, 'wb')
            # 对file_bit字节对象进行base64解码，得到原始的二进制数据并写入文件
            fp.write(base64.b64decode(file_bit.encode()))
            fp.close()
            return {'message': 'Upload Success!', 'upload_file': upload_filename}
        # 如果缺少'upload_filename'或者'file_bit'则报错
        else:
            return {'error': 'need upload_filename and file_bit'}
    # 没有上传JSON数据则报错
    else:
        return {'error': 'no json data'}
            
# 下载文件的路由'download', 限制只能使用POST请求
@node.route('/download', methods=['POST'])
def download():
    client_post_data = request.json
    # 如果有json数据
    if client_post_data:
        # 提取'download_filename'的值
        try:
            download_filename = client_post_data.get('download_filename')
        except AttributeError:
            return {'error': base64.b64encode('json format error'.encode()).decode()}
        # 如果'download_filename'的值不为空，则根据文件名打开本地对应的文件
        if download_filename:
            img_path = f'{parrent_dir}{os.sep}{download_filename}'
            try:
                # 以二进制方式读取文件
                with open(img_path, 'rb') as f:
                    img_bytes = f.read()
                # 通过Base64对二进制进行编码    
                img_base64 = base64.b64encode(img_bytes).decode()
                return {'message': f'{download_filename}下载成功!', 'img_base64':img_base64}
            except:
                # 未找到文件则返回'no_file_error'错误消息
                return {'no_file_error': 'download file not exist'}
        # 如果缺少'download_filename'
        else:
            return {'error': 'need download_filename'}
    # 没有上传JSON数据则报错
    else:
        return {'error': 'no json data'}
        


if __name__ == "__main__":
    # 运行Flask
    node.run(host='0.0.0.0', port=8080)