import paramiko

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.10.1.222', port=22, username='root', password='cisco123', timeout=5, compress=True)
stdin,stdout,stderr = ssh.exec_command('ls')
x = stdout.read().decode()
print(x)