#!/usr/bin/env python3
from difflib import Differ

def diff_txt(prev_config, current_config):
    """
    比较最近两次的设备配置

    参数：
        prev_config(str): 上一次的配置
        current_config(str): 当前的配置
    返回：
        文本：设备配置比对的结果
    """
    prev_config_list = prev_config.split('\n')
    current_config_list = current_config.split('\n')
    result = Differ().compare(prev_config_list, current_config_list)
    compare_result = '\n'.join(list(result))
    return compare_result


if __name__ == '__main__':
    # flake8: noqa
    txt_1 = "\r\nBuilding configuration...\r\n\r\nCurrent configuration : 2406 bytes\r\n!\r\nversion 15.2\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\n!\r\nhostname R1\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r"
    txt_2 = "\r\nBuilding configur...\r\n\r\n : 2407 bytes\r\n!\r\nversion 15.2\r\nservice timestamps debug datetime msec\r\nservice timestamps log datetime msec\r\n!\r\nhostname R1\r\n!\r\nboot-start-marker\r\nboot-end-marker\r\n!\r\n!\r\n!\r\nno aaa new-model\r\n!\r\n!\r\n!\r\n!\r\n!\r\n!\r"
    res=diff_txt(txt_1, txt_2)
    print(res)