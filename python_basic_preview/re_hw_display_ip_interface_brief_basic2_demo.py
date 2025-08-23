import re

# ~ display_ip_interface_brief_line = "Vlanif20							20.1.1.254/24			up(s)			up"

# ~ ipv4_basic = r"(?:\d{1,3}\.){3}\d{1,3}/\d+"
# ~ # (?:\(s\))?  表示(s)有可能出现，也有可能不出现
# ~ pattern = fr"^([A-Z]\S+\d+)\s+({ipv4_basic})\s+(\*?down|up(\(s\))?)\s+(\*?down|up)"

# ~ re_result = re.match(pattern, display_ip_interface_brief_line)
# ~ print(re_result)

# ~ if re_result:
	# ~ result_list = re_result.groups()
	# ~ print(result_list)

pattern = fr"(cat(fish)?)"
res = re.match(pattern,"catfish")
print(res.groups())
#('catfish', 'fish')

#(?:fish)只对fish做匹配，而不提取匹配到的结果
pattern = fr"(cat(?:fish)?)"
res = re.match(pattern,"catfish")
print(res.groups())
#('catfish',)
