import logging
logging.getLogger('kamene.runtime').setLevel(logging.ERROR)
from kamene.all import *


ping_pkt=IP(dst='10.10.1.200')/ICMP()
ping_res=sr1(ping_pkt,timeout=2,verbose=False)
print(ping_res)
if ping_res:
    print('OK')
else:
    print('Failed')

# def qytang_ping(ip):
#     if ping_result:
#         print('Yes')
#     else:
#         print('Failed')
#
# if __name__ == '__main__':
#     result=qytang_ping('192.21.5.254')