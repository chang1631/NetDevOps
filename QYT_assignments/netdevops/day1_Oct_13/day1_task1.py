#!/usr/bin/env python3
from pathlib import Path
import os,sys, requests, re
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

# 头部信息txt文件所在路径
header_txt = f'{parrent_dir}{os.sep}http_req_header.txt'

# 图片下载路径
save_path = f'{parrent_dir}{os.sep}download_img{os.sep}'

def header_txt_dict(txt_file):
    '''
    将包含HTTP头部信息的txt文件转换为Python字典

    参数:
        txt_file(str): 文本文件所在路径
    返回：
        HTTP头部信息字典
    '''
    # 用于存储头部信息的字典
    header_dict = {}
    
    # 遍历文本文件的每一行
    with open(txt_file, 'r') as txt:
        for line in txt:
            line = line.strip()

            # 基于":"将头部信息进行拆分
            if ':' in line:
                key, value = line.split(':',1)
                header_dict[key.strip()] = value.strip()
    return header_dict

def download_img(img_url, header_txt, save_path, img_name):
    '''
    下载URL中的图片至指定目录中
    
    参数：
        img_url(str): 图片的URL
        header_txt(str):  HTTP请求头部信息文本文件所在路径
        save_path(str): 图片的存储路径
        img_name(str): 图片的命名
    '''
    # 发起特定HTTP头部的请求并下载
    try:
        r = requests.get(img_url, headers=header_txt_dict(header_txt))
        # 通过正则表达式判断HTTP状态码
        # 如果HTTP状态码为2XX,则获取图片
        # 状态码不是2XX的则打印失败信息
        if re.match(r'^2\d+', str(r.status_code)):
            # 获取图片的二进制流           
            img_bin = r.content
            # 在指定目录中根据命名新建图片文件并写入图片的二进制流
            img_file = open(f'{save_path}{img_name}','wb')
            img_file.write(img_bin)
            img_file.close()
            print(f'图片下载成功: {save_path}{img_name}')
        else:
            print(f'图片获取失败,HTTP响应:{str(r.status_code)}')
    except Exception as e:
        print(f'发生错误: {str(e)}')


if __name__ == '__main__':
    from pprint import pprint
    # 图片的URL信息
    img_url = 'https://qytsystem.qytang.com/static/images/logo.jpg'

    # 打印HTTP头部信息字典
    http_header_dict=header_txt_dict(header_txt)
    print('='*20+'HTTP Request头部信息'+'='*20)
    pprint(http_header_dict)
    print()

    # 下载图片
    download_img(img_url, header_txt, save_path, 'qyt_log.jpg')