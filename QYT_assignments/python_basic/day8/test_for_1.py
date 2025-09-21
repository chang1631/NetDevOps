# 方案一:不用函数解决
list1 = ['aaa', 111, (4, 5), 2.01]
list2 = ['bbb', 333, 111, 3.14, (4, 5)]

# 遍历list1中的元素并判断是否和list2中的元素相同
for item in list1:
    if item in list2:
        print(str(item) + ' in List1 and List2')
    else:
        print(str(item) + ' only in List1')



