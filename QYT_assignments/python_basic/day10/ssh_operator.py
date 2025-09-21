import paramiko

def qytang_ssh(ip, username, password, port=22, cmd='ls'):
    """
    通过SSH远程连接到Linux主机并执行指定命令
    参数：
        ip(str): 设备IPv4地址
        username(str): SSH用户名
        password(str): SSH密码
        port(int): SSH端口号，默认值为22
        cmd(str): 登录设备后执行的命令，默认值为ls
    返回:
        命令执行的结果或False
    """
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'正在通过SSH连接设备{ip}...')
    try:
        # 尝试对设备进行SSH连接
        ssh.connect(ip, port, username, password, timeout=5, compress=True)
        print(f'登录成功\n正在执行命令{cmd}\n')
        stdin,stdout,stderr = ssh.exec_command(cmd)
        cmd_result = stdout.read().decode()
        ssh.close()
        return cmd_result
    # 抛出错误：无法连接    
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(f'无法通过SSH连接至设备{ip} (SSH端口{port}未开放)\n')
        return False
    # 抛出错误：账户认证失败  
    except paramiko.ssh_exception.AuthenticationException:
        print(f'用户名或密码错误！\n')
        return False
    # 抛出其他错误
    except Exception as msg:
        print(f'连接设备{ip}时发生错误：{msg}')
        return False

    
if __name__ == '__main__':
    print(qytang_ssh('10.10.1.250', 'root', 'c2isco123',cmd='ls'))
    # print(qytang_ssh('10.10.1.222', 'root', 'cisco123', cmd='pwd'))