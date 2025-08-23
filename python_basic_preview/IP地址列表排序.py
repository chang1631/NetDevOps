import ipaddress

ip_list = ['172.16.12.123',
'10.1.1.34',
'172.16.12.3',
'172.16.12.234',
'172.16.12.12',
'192.168.1.123',
'172.16.12.23',
]

res = sorted(ip_list, key = lambda ip:ipaddress.ip_address(ip))
print(res)
