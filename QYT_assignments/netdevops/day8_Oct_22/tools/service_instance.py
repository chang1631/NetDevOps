# atexit用于注册程序退出时要执行的函数。
import atexit
# pyVim 是其中负责“连接 vCenter / ESXi 会话”的部分
#  SmartConnect用于与 vCenter Server 或 ESXi 主机建立连接会话
from pyVim.connect import SmartConnect, Disconnect


def connect(vchost, vcusername, vcpassword, port=443):
    """
    连接到vCenter主机

    参数：
        vchost(str): vCenter主机的IP地址
        vcusername(str): vCenter用户名
        vcpassword(str): vCenter密码
        port(int): 端口号
    """
    # 定义变量用于存储vCenter Server的会话实例
    service_instance = None

    # 连接到vCenter或ESXi
    try:
        service_instance = SmartConnect(protocol='https',
                                        host=vchost,
                                        user=vcusername,
                                        pwd=vcpassword,
                                        disableSslCertValidation=True)

        # 断开连接
        atexit.register(Disconnect, service_instance)
    except IOError as io_error:
        print(io_error)

    if not service_instance:
        raise SystemExit("Unable to connect to host with supplied credentials.")

    return service_instance