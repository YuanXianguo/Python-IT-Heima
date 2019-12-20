import time, os, random
from multiprocessing import Pool

def run(num):
    print('子进程{}启动--{}'.format(num, os.getpid()))
    start = time.perf_counter()
    time.sleep(random.choice([1, 2, 3]))
    print('子进程{}结束--{}，耗时{:.6f}'.format(num, os.getpid(), time.perf_counter()-start))

if __name__ == '__main__':
    print('父进程启动')
    # 创建进程池，默认大小是CPU内核，可以传入同时执行进程的数量
    pp = Pool()
    for i in range(5):
        # 创建进程，放入进程池统一管理
        pp.apply_async(run, args=(i,))
    # 在调用join之前必须先调用close
    pp.close()
    pp.join()
    # 注意全局变量在多进程中不能共享
    print('父进程结束')
