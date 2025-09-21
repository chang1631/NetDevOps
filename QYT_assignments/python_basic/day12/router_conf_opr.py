import paramiko
import time
import re
import sys

from paramiko import channel

def qytang_multicmd(ip, username, password, cmd_list=[], enable='', wait_time=2, verbose=True, port=22):
    """
    根据传入的命令清单，对路由器执行相关配置
    参数：
        ip(str): 路由器的管理IP地址
        username(str): SSH用户名
        password(str): SSH密码
        cmd_list(list): 命令清单
        enable(str): enable密码，默认为空
        wait_time: 控制等待网络设备返回信息的时间，默认为2秒
        verbose: 决定是否打印网络设备返回信息, True为打印， False为不打印 
        port(int): SSH端口号，默认值为22
    返回：
        字典: 包含了show命令与其对应的执行结果
    """
    # 如果发现cmd_list有非字符串的元素，则直接退出程序
    for cmd in cmd_list:
        if not isinstance(cmd,str):
            print(f'命令清单中的{cmd}不是字符串\n程序已退出')
            sys.exit()

    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port, username, password, timeout=5, compress=True)
        # 激活交互式shell
        chan = ssh.invoke_shell()
        time.sleep(wait_time)
        # 获取当前的命令模式
        cmd_mode = chan.recv(2048).decode()
        # 用正则表达式判断当前是否为用户模式
        user_mode = re.match(r'[\s\S]*>$',cmd_mode)
        # 如果当前是用户模式并且有enable密码参数传入，则输入enable密码
        if user_mode and enable != '':
            # 进入enable模式
            chan.send('enable'.encode())
            chan.send(b'\n')
            time.sleep(wait_time)
            # 接收enable命令的返回信息
            chan.recv(2048).decode()
            # 输入enable密码
            chan.send(enable.encode())
            chan.send(b'\n')
            time.sleep(wait_time)
            # 接收enable密码的返回信息
            enable_auth_res = chan.recv(2048).decode()
            # 如果返回的是Password:提示符, 说明enable密码错误，直接退出程序
            if r'Password:' in enable_auth_res:
                print('enable密码不正确！\n程序已退出')
                sys.exit()

        show_result = {}
        # 逐条执行cmd_list中的命令
        for cmd in cmd_list:
            chan.send(cmd.encode())
            chan.send(b'\n')
            time.sleep(wait_time)
            # 将命令的返回结果赋值给一个变量
            dev_feedback = chan.recv(2048).decode()
            # 定义show命令相关的正则表达式pattern
            is_show_cmd = re.match(r'^[sh|show]',cmd)
            # 如果是show命令且返回正常的结果，则进一步执行操作
            if is_show_cmd and r'% Invalid input' not in dev_feedback:    
                # 如果输出中有--More--关键字，则发送空格显示下一页信息并把之前的输出和后续输出进行拼接
                match_more = re.match(r'[\s\S]*--More--(\s)*$', dev_feedback)
                while match_more:
                    chan.send(b' ')
                    time.sleep(wait_time)
                    dev_feedback += chan.recv(2048).decode()
                    match_more = re.match(r'[\s\S]*--More--(\s)*$', dev_feedback)
                # 如果返回正常的结果则通过正则表达式提取以命令开头和以主机名全局模式提示符为结尾的中间部分并存入字典show_result
                # 以cmd作为字典的key，dev_feedback作为字典的value
                show_result[cmd] = re.findall(fr'^{cmd}([\S\s]*)\s+[\d\w]+#$',dev_feedback)[0]

            # 如果verbose开启则打印设备返回的信息
            if verbose: 
                print(dev_feedback)
        chan.close()
        ssh.close()
        print("所有命令执行结束")
        return show_result
    # 处理各种异常情况    
    except TimeoutError:
        print('连接超时!')
        return None
    except paramiko.ssh_exception.AuthenticationException:
        print('用户名或密码错误，认证失败!')
        return None
    except paramiko.ssh_exception.NoValidConnectionsError:
        print('未能连接到指定的SSH端口，请检查目的端口是否开启！')
        return None
    except Exception as e:
        print(f'发生异常：{str(e)}')
        return None

        




if __name__ == '__main__':
    conf_list = ['show ver', 'conf t', 'router ospf 1','router-id 100.100.100.100','network 10.10.1.0 0.0.0.255 area 0']
    conf_res = qytang_multicmd('10.10.1.101', 'admin', 'Cisc0123', conf_list, enable='abcdef')

    # if conf_res is not None:
    #     for cmd,result in conf_res.items():
    #         print('='*80)
    #         print(f'命令{cmd}的执行结果：\n{result}\n')