from kamene.all import *
import logging
logging.getLogger("kamenem.runtime").setLevel(logging.ERROR)
ping_pkt = IP(dst='10.10.1.254')/ICMP()
ping_result = sr1(ping_pkt, timeout=2, verbose=False)

if ping_result:
    print('Yes')