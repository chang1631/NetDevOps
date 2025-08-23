import re
###1.转义符
# ~ "."表示匹配任何内容

# ~ res = re.match('cmd.exe','cmdaexe')
# ~ print(res)

# ~ 使用转义符"\", "\."表示"."本身

# ~ res = re.match('cmd\.exe','cmd.exe')
# ~ print(res)


### 2.多种字符
# ~ \d 0-9中任意一个数字
# ~ \w 任意一个大小写字母、数字或者下划线
# ~ \s 空格、制表符、换页符等空白字符
# ~ \S 任何非空白字符
# ~ . 换行符“\n”以外的任意一个字符

# ~ res= re.match('\d\d\d','123')
# ~ res= re.match('\d\d\d','12a')
# ~ res= re.match('\d\d\w','12a')
# ~ print(res)

# ~ res=re.match('\s','\r')
# ~ print(res)

# ~ res=re.match('.','\n')
# ~ print(res)

# ~ res=re.match('\S','    ')
# ~ print(res)      
# ~ 结果为None, \S不能匹配空格


###3.自定义多种字符
# ~ [a-d]匹配a~d之前的字母(包含a和d)
# ~ res=re.match('a[a-d]c','abc')
# ~ print(res)    

# ~ [0-9]匹配0~9之前的数字
# ~ res=re.match('a[0-9]c','a5c')
# ~ print(res)    

# ~ [^a-z]匹配a~z以外的字符
# ~ res=re.match('a[^a-z]c','atc')
# ~ print(res)    

# ~ res=re.match('a[^a-z]c','a4c')
# ~ print(res)

 # ~ [\s\S]*匹配所有
# ~ res=re.match('a[\s\S]*c','a \n\t\rc')
# ~ print(res)


###4.匹配次数
# ~ {n} 重复n次
# ~ res = re.match('ba(na){3}', 'bananana') 	#na重复3次
# ~ print(res)

# ~ {m,n} 重复m~n次
# ~ res = re.match('ba(na){3,6}', 'banananananana') 	#na至少重复3次，最多重复6次
# ~ print(res)

# ~ {m,} 至少重复m次
# ~ res = re.match('ba(na){2,6}', 'bana') 	#na至少重复2次
# ~ print(res)    #None

# ~ res = re.match('ba(na){2,6}', 'bananana') 	#na至少重复2次
# ~ print(res)

# ~ ? 出现0或1次
# ~ res = re.match('ba(na)?', 'bananana') 		#na出现0或1次
# ~ print(res)

# ~ res = re.match('ba(na)?', 'ba') 		#na出现0或1次
# ~ print(res)

# ~ + 至少出现1次
# ~ res = re.match('ba(na)+', 'ba') 		#na出现0或1次
# ~ print(res)		#None

# ~ res = re.match('ba(na)+', 'bana') 		#na出现0或1次
# ~ print(res)
		
# ~ * 不出现或出现任意次
# ~ res = re.match('ba(na)*', 'ba') 		#na不出现或者出现任意次
# ~ print(res)

# ~ res = re.match('ba(na)*', 'bananana') 		#na不出现或者出现任意次
# ~ print(res)

###思考
#匹配IP地址
# ~ ip_match = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '8.8.8.8')
# ~ print(ip_match)

# ~ ip_match = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '1.10.100.254')
# ~ print(ip_match)

# ~ ip_match = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '192.168.12.1')
# ~ print(ip_match)

ip_match = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '255.255.255.2555')
print(ip_match)

#匹配MAC地址
# ~ mac_match = re.match('([0-9,A-F]{2}[\-,\:]{1}){5}[0-9,A-F]{2}','00-50-56-C0-00-08')
# ~ print(mac_match)

# ~ mac_match = re.match('([0-9,A-F]{2}[\-,\:]{1}){5}[0-9,A-F]{2}','00:50:56:C0:00:08')
# ~ print(mac_match)

# ~ mac_match = re.match('([0-9,A-F]{2}[\-,\:]{1}){5}[0-9,A-F]{2}','00-50-56')
# ~ print(mac_match)		#None

# ~ mac_match = re.match('([0-9,A-F]{2}[\-,\:]{1}){5}[0-9,A-F]{2}','0-50-56-C0-00-08')
# ~ print(mac_match)		#None


###5.代表抽象意义
# ~ ^与字符串开始的地方匹配
# ~ res = re.match('^qyt','qytangccies')
# ~ print(res)		#<re.Match object; span=(0, 3), match='qyt'>

# ~ res = re.match('^opqyt','qytangccies')
# ~ print(res)		#None

# ~ $与字符串结束的地方匹配
# ~ res = re.match('.*ccies$','qytangccies')	#".*"代表ccies之前可以是任意字符；ccies$字符串必须以ccies结尾
# ~ print(res)
# ~ <re.Match object; span=(0, 11), match='qytangccies'>

# ~ \b用来匹配一个单词的开头或结尾的位置
#“单词边界”是单词字符（字母、数字或下划线）\w 和 非单词字符（如空格、标点或字符串边界） 之间的位置
#注：正则字符串中 \b 是特殊字符（退格符），所以 一定要用原始字符串：E.g.: r"...\b"
#精确匹配一个单词
# ~ res = re.findall(r'\bfood\b','food')
# ~ print(res)
# ~ ['food']

# ~ res = re.findall(r'\bfood\b',', food bar')
# ~ print(res)
# ~ #None

#精确匹配一个单词的开头
# ~ res = re.match(r'\bfood','foodbar')
# ~ print(res)
#<re.Match object; span=(0, 4), match='food'>

# ~ res = re.match(r'\bfood','sfoodbar')
# ~ print(res)
#None

#精确匹配一个单词的结尾
# ~ res = re.findall(r'food\b','barfood')
# ~ print(res)
#['food']

# ~ res = re.findall(r'food\b','barfoodbar')
# ~ print(res)
#[]

# ~ re.match(pattern, string)：只在字符串开头进行匹配
# ~ -它只尝试从字符串的第一个字符开始匹配。
# ~ -如果正则表达式没有匹配开头，就返回 None。

# ~ re.findall(pattern, string)：查找所有匹配内容，返回列表
# ~ -它会扫描整个字符串，找出所有匹配项。
# ~ -返回的是一个字符串列表（或字符串元组列表，视正则是否有分组而定）。

###6.表达式关系
# ~ | 匹配时表示“或”
# ~ ()匹配次数时在括号内的字符表示整体；提取匹配结果时，括号内的内容可以被单独得到
# ~ res = re.match('root|Root', 'root')
# ~ print(res)
#<re.Match object; span=(0, 4), match='root'>

# ~ res = re.match('root|Root', 'Root')
# ~ print(res)
#<re.Match object; span=(0, 4), match='Root'>


###Sub and Split
# ~ split过滤匹配到的内容
res = re.split('---','aaa---bbb---ccc')
print(res)		#['aaa', 'bbb', 'ccc']

res = re.split('[-=]','aaa=bbb-ccc=ddd')		#匹配-或=并过滤
print(res)		#['aaa', 'bbb', 'ccc']

# ~ sub用于替换匹配到的内容
res = re.sub('--','...','aaa--bbb-cc')
print(res)		#aaa...bbb-cc
