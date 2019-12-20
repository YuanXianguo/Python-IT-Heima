from multiprocessing import Process
import time, os, random

class MyProcess(Process):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def run(self):
        print('子进程{}启动--{}'.format(self.num, os.getpid()))
        start = time.perf_counter()
        time.sleep(random.choice([1, 2, 3]))
        print('子进程{}结束--{}，耗时{:.6f}'.format(self.num, os.getpid(), time.perf_counter() - start))
