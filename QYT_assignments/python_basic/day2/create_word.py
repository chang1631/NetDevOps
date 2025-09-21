word = input("请输入一个英语单词：")

#提取单词的首字母
first_letter = word[0]

#提取单词的剩余部分
other_letters = word[1:]

#将拼接的结果赋值给变量new_word
new_word = other_letters + "-" + first_letter + "y"

print("创造的新单词位为：" + new_word)