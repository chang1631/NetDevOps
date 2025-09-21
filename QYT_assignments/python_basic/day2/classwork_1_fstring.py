department1 = 'Security'
department2 = 'Python'
depart1_m = 'cq_bomb'
depart2_m = 'qinke'
COURSE_FEES_SEC = 456789.12456
COURSE_FEES_Python = 1234.3456

#补齐被删除的代码之f-string方法
line1 = f'Department1 name:{department1:<12} Manager:{depart1_m:<10} COURSE FEES:{COURSE_FEES_SEC:<10.2f} The End!'
line2 = f'Department2 name:{department2:<12} Manager:{depart2_m:<10} COURSE FEES:{COURSE_FEES_Python:<10.2f} The End!'

length = len(line1)
print('='*length)
print(line1)
print(line2)
print('='*length)