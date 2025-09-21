import paramiko

def qytang_ssh(ip, username, password, port=22, cmd='ls'):
    """
    通过SSH远程连接到Linux主机并执行指定命令
    返回命令执行的结果
    """
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password, timeout=5, compress=True)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    x = stdout.read().decode()
    ssh.close()
    return x

if __name__ == '__main__':
    print(qytang_ssh('10.10.1.222', 'root', 'cisco123'))
    print(qytang_ssh('10.10.1.222', 'root', 'cisco123', cmd='pwd'))