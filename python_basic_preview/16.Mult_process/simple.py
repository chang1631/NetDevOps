from module import qyt_multi
from multiprocessing import cpu_count, Pool as ProcessPool
from multiprocessing.pool import ThreadPool
from multiprocessing import freeze_support
import random
from datetime import datetime

if __name__=='__main__':
    start_time = datetime.now()
    #多进程
    freeze_support()
    pool = ProcessPool()
    cpus = cpu_count()
    #多线程
    # pool = ThreadPool()
    results = []
    for i in range(0,15):
        x = random.randint(1,10)
        y = random.randint(1,10)
        z = random.randint(1,10)
        # result = pool.apply_async(qyt_multi, args=(x,y,z))
        result = pool.apply_async(qyt_multi, args=(x,y,z))
        results.append(result)

    pool.close()
    pool.join()
    end_time = datetime.now()

    for i in results:
        print(i.get())
    print(end_time - start_time)