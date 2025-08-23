def find_index(obj, index):
    print(obj[index])

if __name__=='__main__':
    import re
    try:
        find_index('qytang',100)
    except:
        print('发生了异常')
    else:
        print("没有任何错误发生！")
    finally:
        print("这个总是要打印的！")