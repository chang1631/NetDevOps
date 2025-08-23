from threading import Thread
from time import sleep, ctime

# 创建Thread的子类
class MyThread(Thread):
    def __init__(self, func, args):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = None

    # 执行流程是这样的：
    #
    # t.start() → Thread.start() 内部会自动调用 run()，但这个调用是在新线程中发生的。
    #
    # 如果你直接调用 t.run()，它会在当前线程执行，不会启动新的线程。
    def run(self):
        self.func(*self.args)

    def getResult(self):
        return self.result


def func(name, sec):
    print('---开始---',name,'时间',ctime())
    sleep(sec)
    print('---结束---',name,'时间',ctime())
    return sec

def main():
    # 创建Thread实例
    t1 = MyThread(func,(1,1))
    t2 = MyThread(func,(2,2))


    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(t1.getResult())
    print(t2.getResult())

if __name__ == '__main__':
    main()