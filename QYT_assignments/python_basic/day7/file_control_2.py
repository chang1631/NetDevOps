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

print('方案二:')
print('文件中包含"qytang"关键字的文件为:')
# topdown=False: 从当前目录中的子目录开始往上层目录遍历
# root: 当前遍历的路径信息
# dirs: 当前遍历的目录中所包含的目录
# files: 当前遍历的目录中所包含的文件
for root, dirs, files in os.walk(os.getcwd(), topdown=False):
    # 遍历当前目录中所有文件
    for file_name in files:
        #拼接完整的文件路径
        file_path = os.path.join(root,file_name)
        # 打开文件并逐行搜索关键字'qytang',一旦搜索到就打印文件名并退出搜索
        with open(file_path) as search_file:
            for line in search_file:
                if 'qytang' in line:
                    print('\t'+file_name)
                    break   

# 完成清理工作
os.chdir('..')
for root, dirs, files in os.walk('test', topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.removedirs('test')