from basic_ssh_operator import qytang_ssh
import re
import hashlib
import time

def qytang_get_config(ip, username='admin', password='Cisc0123', port=22):
    """
    通过SSH远程连接至网络设备并捕获设备的配置信息
    参数：
        ip(str): 目标主机IPv4地址
        username(str): SSH用户名
        password(str): SSH密码
        port(int): SSH端口号，默认值为22
    返回:
        run_conf_ex(str)：捕获到的设备配置信息
        False(bool): 未捕获到设备配置
        None: 发生错误
    """
    # 定义正则表达式pattern用于捕获设备配置中hostname至end之间的部分
    conf_pattern = r'hostname[\s\S]*end'
    try:
        show_run_result =  qytang_ssh(ip, username, password, port, cmd='show run')
        # 通过正则匹配捕获到的设备配置信息
        match = re.search(conf_pattern, show_run_result)
        if match:
            run_conf_ex = match.group(0)
            return run_conf_ex
        else:
            print("未捕获到设备配置")
            return False
    except Exception as errmsg:
        print(f'发生错误：{errmsg}!')
        return

def qytang_check_diff(ip, username='admin', password='Cisc0123', port=22):
    """
    每隔5秒捕获一次网络设备的配置信息并进行MD5哈希运算；
    通过计算出的MD5值与之前一次计算出的MD5值进行比对以监控设备配置的改变
    参数：
        ip(str): 目标主机IPv4地址
        username(str): SSH用户名
        password(str): SSH密码
        port(int): SSH端口号，默认值为22
    返回:
        prev_md5: 原设备配置信息的MD5值
        md5_value: 设备配置信息改变后的MD5值
    """
    prev_md5 = ''
    while True:
        current_run_conf = qytang_get_config(ip, username, password, port)
        # 如果没有捕获到设备配置信息则直接退出
        if not current_run_conf:
            break
        # 创建MD5算法的哈希对象并计算捕获到的设备配置信息的MD5值
        md5_calc = hashlib.md5()
        md5_calc.update(current_run_conf.encode())
        md5_value = md5_calc.hexdigest()
        if prev_md5 == '':
            prev_md5 = md5_value
        elif prev_md5 == md5_value:
            print(md5_value)
        else:
            print('MD5 value changed')
            return prev_md5, md5_value
            break
        time.sleep(5)



if __name__ == '__main__':
    qytang_check_diff('10.10.1.101')