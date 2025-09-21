department1 = 'Security'
department2 = 'Python'
depart1_m = 'cq_bomb'
depart2_m = 'qinke'
COURSE_FEES_SEC = 456789.12456
COURSE_FEES_Python = 1234.3456

#补齐被删除的代码之format方法
line1 = 'Department1 name:{0:<12} Manager:{1:<10} COURSE FEES:{2:<10.2f} The End!'.format(department1, depart1_m, COURSE_FEES_SEC)
line2 = 'Department2 name:{0:<12} Manager:{1:<10} COURSE FEES:{2:<10.2f} The End!'.format(department2, depart2_m, COURSE_FEES_Python)

length = len(line1)
print('='*length)
print(line1)
print(line2)
print('='*length)