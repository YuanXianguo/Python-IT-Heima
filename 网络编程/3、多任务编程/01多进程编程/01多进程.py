import time
from multiprocessing import Process
import os

def run(num):
    while True:  # os.getpid()获得进程号,os.getpid()获得父进程号
        print(num, os.getpid(), os.getppid())
        time.sleep(0.5)

if __name__ == '__main__':
    print('主（父）进程启动')
    # 创建子进程，target说明进程进程执行的任务
    p = Process(target=run, args=(0,))
    p.start()

    while True:
        print(1, os.getpid())
        time.sleep(0.5)
