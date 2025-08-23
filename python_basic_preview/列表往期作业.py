import re

port_list=['eth 1/101/1/42','eth 1/101/1/26','eth 1/101/1/23','eth 1/101/1/7',
'eth 1/101/2/46','eth 1/101/1/34','eth 1/101/1/18','eth 1/101/1/13','eth 1/101/1/32',
'eth 1/101/1/25','eth 1/101/1/45','eth 1/101/2/8']

# ~ 定义用于抓取接口编号数字部分的正则表达式
port_num_pattern = r'^eth (\d)/(\d+)/(\d)/(\d+)'

# ~ 定义一个空列表用于存储匹配到的接口编号列表
pt_num_list = []

# ~ 遍历port_list并通过正则表达式抓取每个接口的编号部分，并将其单独纳入一个列表
for pt in port_list:
	res = re.match(port_num_pattern, pt).groups()
	# ~ 将正则表达式捕获到的每个接口的编号列表添加至pt_num_list
	pt_num_list.append(list(res)) 

# ~ 对pt_num_list中的列表，根据接口编号的第3位和第4位(即每个嵌套列表的第2个元素和第3和元素)进行排序	
sorted_list = sorted(pt_num_list, key=lambda x: (int(x[2]),int(x[3])))

# ~ 定义一个空列表用于存储排序后的接口信息
new_port_list = []

for x in sorted_list:
	index = 0
	interface_num = ''
	for y in x:
		# ~ 如果不是编号列表中的最后一个元素则在末尾添加/
		if index != len(x) - 1: 
			interface_num = interface_num + y + '/'
			index += 1
		else:
			interface_num = interface_num + y
	new_port_list.append('eth ' + interface_num)
	
print(new_port_list)

