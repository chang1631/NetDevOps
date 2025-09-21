from kamene.all import *
import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)

class QYTPING:
    """表示一个Ping测试

    属性：
        dstip (str): 目标IPv4地址
        length (int): 负载长度
        srcip (str): 源IPv4地址
    """
    def __init__(self,dstip, length=100, srcip=''):
        self.dstip = dstip
        self.length = length
        self.srcip = srcip
    
    def one(self):
        """
        发送一个PING包

        返回: True或者False
        """
        ping_pkt = IP(dst=self.dstip)/ICMP()
        ping_result = sr1(ping_pkt, timeout=2, verbose=False)
        # 如果接收到了ICMP的回包且类型为echo reply则说明可以ping通
        icmp_layer = ping_result.getlayer(ICMP) if ping_result else None
        if icmp_layer and icmp_layer.type == 0:
            print(f'{self.dstip} 可达!')
            return True
        else:
            print(f'{self.dstip} 不可达!，请检查网络连接或设备状态！\n')
            return False
    
    def ping(self, sucs_symb = '!', fail_symb = '.'):
        """
        发送五个PING包
        参数:
            sucs_symb (str): PING成功时打印的符号
            fail_symb (str): PING失败时打印的符号
        """
        # Raw ICMP包的负载部分，用于设定负载长度
        if self.srcip != '':
            ping_pkt = IP(dst=self.dstip,src=self.srcip)/ICMP()/Raw(b'x' * self.length)
        else:
            ping_pkt = IP(dst=self.dstip)/ICMP()/Raw(b'x' * self.length)
        for pkt_num in range(0,5):
            ping_result = sr1(ping_pkt, timeout=2, verbose=False)
            icmp_layer = ping_result.getlayer(ICMP) if ping_result else None
            if icmp_layer and icmp_layer.type == 0:
                # end=''不换行打印结果
                # flush=True 逐个字符进行打印
                print(sucs_symb, end='', flush=True) 
            else:
                print(fail_symb, end='', flush=True)
        #打印用于换行
        print()

    # 格式化显示实例信息
    def __str__(self):
        # 如果设定了源地址srcip参数就在实例的基本信息中显示设定的源地址信息
        if self.srcip != '':
            return '<%s => srcip: %s, dstip: %s, size: %s>' % (self.__class__.__name__,self.srcip, self.dstip, self.length)
        else:    
            return '<%s => dstip: %s, size: %s>' % (self.__class__.__name__, self.dstip, self.length)

class NewPing(QYTPING): 
    """表示一个Ping测试

    继承QYTPING类
    """

    def ping(self):
        """
        基于QYTPING的ping函数，修改了PING成功和失败时打印的符号
        """
        QYTPING.ping(self, r'+', r'?')


if __name__ == '__main__':
    ping = QYTPING('10.10.1.254')
    total_len = 70

    def print_new(word, s='-'):
        print('{0}{1}{2}'.format(s * int((total_len - len(word))/2), word, s * int((70 - len(word))/2)))
    print_new('print class') 
    print(ping) # 打印类
    print_new('ping one for sure reachable') 
    ping.one() # Ping一个包判断可达性
    print_new('ping five') 
    ping.ping() # 模拟正常ping程序ping五个包，'!'表示通，'.'表示不通
    print_new('set payload length') 
    ping.length = 200 # 设置负载长度
    print(ping) # 打印类
    ping.ping() # 使用修改长度的包进行ping测试
    print_new('set ping src ip address') 
    ping.srcip = '192.168.1.123' # 修改源IP地址
    print(ping) # 打印类
    ping.ping() # 使用修改长度又修改源的包进行ping测试
    print_new('new class NewPing', '=') 
    newping = NewPing('10.10.1.254') # 使用新的类NewPing(通过继承QYTPING类)产生的实例！
    newping.length = 300
    print(newping) # 打印类
    newping.ping()  # NewPing类自定义过ping()这个方法，'+'表示通，'?'表示不通

    print_new('set newping dst ip address')
    newping.dstip = '20.20.20.20' # 修改newping的目标地址为一个不存在的IP地址
    print(newping)
    newping.ping()