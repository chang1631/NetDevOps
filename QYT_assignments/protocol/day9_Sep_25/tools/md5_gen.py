#!/usr/bin/env python3
import hashlib

def get_hash(config):
    """
    为配置信息计算MD5值

    参数：
        config(str): 配置信息
    返回：
        MD5值
    """
    m = hashlib.md5()
    m.update(config.encode())
    md5_value = m.hexdigest()

    return md5_value

if __name__ == '__main__':
    txt_1 = "\r\nBuilding configuration...\r\n\r\nCurrent configuration : 2406 bytes\r\n!\r\nversion 15.2\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\n!\r\nhostname R1\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r"

    print(get_hash(txt_1))