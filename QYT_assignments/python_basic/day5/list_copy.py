l1 = [4,5,7,1,3,9,0]

# 对列表l1进行拷贝并赋值给l2
l2 = l1[:]

# 对l2进行排序 (由小到大)
l2.sort()

# 打印l1和l2中的每一个元素
for i in range(len(l1)):
    print(l1[i],l2[i])