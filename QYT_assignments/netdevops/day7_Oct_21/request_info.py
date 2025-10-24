#!/usr/bin/env python3
import requests

# 发起requests会话
client = requests.session()

# HTTP Request头部信息
headers = {'Accept': 'application/yang-data+json',
           'Content-Type': 'application/yang-data+json'}

# 将设备的登录信息存入字典
devices = {'c8kv1':{'ip':'10.10.1.101',
           'username':'admin',
           'password':'Cisc0123'}
}