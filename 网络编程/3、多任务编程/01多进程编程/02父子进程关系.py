import time
from multiprocessing import Process

num = 100
def run():
    print('子进程启动')
    time.sleep(1)
    global num
    num += 1
    print('子进程结束')

if __name__ == '__main__':
    print('父进程启动')

    p = Process(target=run)
    p.start()
    p.join()
    print('父进程结束{}'.format(num))
