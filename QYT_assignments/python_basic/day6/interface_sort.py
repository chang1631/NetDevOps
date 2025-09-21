port_list = ['eth 1/101/1/42','eth 1/101/1/26','eth 1/101/1/23','eth 1/101/1/7','eth 1/101/2/46','eth 1/101/1/34','eth 1/101/1/18','eth 1/101/1/13','eth 1/101/1/32','eth 1/101/1/25','eth 1/101/1/45','eth 1/101/2/8']

# intf.split()[1] 提取接口的编号字符串
# .split('/') 再基于'/'符号将编号字符串拆分成一个列表(列表中的数字仍然是字符串类型)
# [int(str_intf) for str_intf in intf.split()[1].split('/')]将列表中字符串类型的数字转换成int类型
# 打印排序的结果
print(sorted(port_list, key=lambda intf:[int(str_intf) for str_intf in intf.split()[1].split('/')]))