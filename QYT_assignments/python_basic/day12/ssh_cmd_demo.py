import paramiko
import time
import re


ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.10.1.101', port=22, username='admin',password='Cisc0123', timeout=5,compress=True)
chan = ssh.invoke_shell()
time.sleep(1)
x = chan.recv(2048).decode()
# 有enable密码的情况
match = re.match(r'[\s\S]*>$',x)
if match:
    print('yes')
# print(x)

chan.send('enable'.encode())
chan.send(b'\n')
time.sleep(2)
x = chan.recv(2048).decode()
# print(x)

chan.send('Cisc0123'.encode())
chan.send(b'\n')
time.sleep(2)
x = chan.recv(2048).decode()
print(x)

chan.send('show version'.encode())
chan.send(b'\n')
time.sleep(2)
x = chan.recv(2048).decode()
match = re.match(r'[\s\S]*--More--(\s)*$',x)
if match:
    # print('yes')
    chan.send(b' ')
    time.sleep(2)
    x = x + chan.recv(2048).decode()
    print(x)
