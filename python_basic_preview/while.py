import time
import signal
import sys

# ~ def sigint_handler(signum,frame):
		# ~ print('接收到管理员的Ctrl + C')
		# ~ print('退出程序')
		# ~ sys.exit()

# ~ signal.signal(signal.SIGINT,sigint_handler)
# ~ while True:
		# ~ time.sleep(2)
		# ~ print('请输入Ctrl + C来停止这个循环')


# ~ x=7
# ~ while x:
		# ~ x=x-1
		# ~ if x%2 !=0:pass
		# ~ print(x,end=' ')

while True:
	name = input('请输入你的名字:')
	if name == 'stop':break
	age = input('请输入你的年龄:')
	print('你好',name, int(age)**2)
