import os
import time
from datetime import datetime 

while True:
    # 将netstat命令捕获到的关于TCP80端口的信息赋值给一个变量
    # -t: 仅显示tcp相关选项
    # -n: 以数字形式显示地址信息
    # -p: 显示建立相关链接的程序名
    # -l: 列出有在 Listen (监听) 的服务状态
    # grep -E ":80([^0-9]|$) 只捕获80端口相关的信息
    is_established = os.popen('netstat -tnpl | grep -E ":80([^0-9]|$)"').read()

    # 如果netstat返回了TCP80端口的信息则打印告警信息并退出循环
    # 否则等待1秒后进行重试
    if is_established.strip():
        # 添加时间戳信息
        open_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('HTTP（TCP/80）服务已经被打开 ' + open_time)
        break
    else:
        print('等待一秒重新开始监控！')
        time.sleep(1)