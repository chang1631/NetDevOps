#!/usr/bin/env python3
from argparse import ArgumentParser, RawDescriptionHelpFormatter

# 添加Usage并初始化ArgumentParser实例
usage = "usage: python Simple_SSH_Client -i ipaddr -u username -p password -c command"
parser = ArgumentParser(
    usage=usage,
    formatter_class=RawDescriptionHelpFormatter, # 关闭usage拼接
    add_help=True # 开启-h帮助信息
    )

# 自定义options标题
parser._optionals.title = 'optional arguments'

# 添加optional arguments
parser.add_argument('-i', '--ipaddr', dest='IPADDR', help='SSH Server', type=str)
parser.add_argument('-u', '--username', dest='USERNAME', help='SSH Username', default='root', type=str)
parser.add_argument('-p', '--password', dest='PASSWORD', help='SSH Password', default='Cisc0123', type=str)
parser.add_argument('-c', '--command', dest='COMMAND', help='Shell Command', default='', type=str)

# 解析用户传入的参数
args = parser.parse_args()