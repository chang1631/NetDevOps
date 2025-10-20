#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import os,sys, requests
# 获取当前文件所在路径
working_dir = Path(__file__)
# 获取当前父目录的路径
parrent_dir = working_dir.parent
# 获取项目的根路径
project_root = parrent_dir.parent

from header_reader import header_txt_dict

# 要爬取的URL
url = 'https://qytsystem.qytang.com/python_enhance/python_enhance_homework'

# 将http_request_headers.txt中的字符串信息转换成字典
request_headers_txt = f'{parrent_dir}{os.sep}http_request_headers.txt'
request_headers_dict = header_txt_dict(request_headers_txt)

# 发起requests会话
client = requests.session()
html_page = client.get(url, headers = request_headers_dict)

# 爬取页面并使用lxml HTML解析器进行解析
my_soup = BeautifulSoup(html_page.text, 'lxml')

print(type(my_soup))