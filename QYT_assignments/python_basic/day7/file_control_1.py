import os
# 在根目录"/"下创建一个新的文件夹QYT_day7用于该作业实验
os.mkdir('/QYT_day7')
os.chdir('/QYT_day7')

# 在"/QYT_day7"目录下创建实验所需的文件和目录
os.mkdir('test')
os.chdir('test')
qytang1 = open('qytang1','w')
qytang1.write('test file\n')
qytang1.write('this is qytang\n')
qytang1.close()
qytang2 = open('qytang2','w')
qytang2.write('test file\n')
qytang2.write('qytang python\n')
qytang2.close()
qytang3 = open('qytang3','w')
qytang3.write('test file\n')
qytang3.write('this is python\n')
qytang3.close()
os.mkdir('qytang4')
os.mkdir('qytang5')

print('方案一:')
print('文件中包含"qytang"关键字的文件为:')
for file_or_dir in os.listdir(os.getcwd()):
    # 判断当前的对象是否为文件
    if os.path.isfile(file_or_dir):
        # 打开文件并逐行搜索关键字'qytang',一旦搜索到就打印文件名并退出搜索
        with open(file_or_dir) as search_file:
            for line in search_file:
                if 'qytang' in line:
                    print('\t'+file_or_dir)
                    break  
    
 # 完成清理工作
os.chdir('..')
for root, dirs, files in os.walk('test', topdown=False):
    # 删除子目录中的所有文件
    for name in files:
        os.remove(os.path.join(root, name))
    # 删除所有子目录
    for name in dirs:
        os.rmdir(os.path.join(root, name))
# 删除当前目录中名字为test的目录
os.removedirs('test')               

