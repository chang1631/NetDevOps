import re

display_ip_interface_brief_line = "Vlanif20							20.1.1.254/24			up			up"
ipv4_basic = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d+"		#匹配IP地址部分X.X.X.X/X
#([A-Z]\S+\d+) 匹配接口名称(首字母大写)
pattern = fr"^([A-Z]\S+\d+)\s+({ipv4_basic})\s+(down|up)\s+(down|up)"
re_result = re.match(pattern, display_ip_interface_brief_line)
print(re_result)

if re_result:
	result_list = re_result.groups()
	print(result_list)

title_list = ['Interface', 'IP address/Mask', 'Physical', 'Protocol']
str_format = "|{:<20} | {:<15} | {:<10} | {:<10}|"
print(str_format.format(*title_list))
print(str_format.format(*result_list))
