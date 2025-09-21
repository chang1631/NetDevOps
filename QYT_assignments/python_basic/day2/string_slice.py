word = " scallywag"

#定义一个变量并赋值关键词"ally"
keyword = "ally" 

#找出"ally"在word中起始index
start_index = word.find(keyword)

#结合起始index和"ally"的长度计算出末尾index
last_index = start_index + len(keyword)

#对word进行切片并把结果赋值给sub_word
sub_word = word[start_index:last_index]

print(sub_word)
