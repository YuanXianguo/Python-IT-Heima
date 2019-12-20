from multiprocessing import Process, Queue
import os, time

def write(q):
    print('子进程启动{}'.format(os.getpid()))
    for c in ['a', 'b', 'c', 'd']:
        q.put(c)
        time.sleep(1)
    print('子进程结束{}'.format(os.getpid()))

def read(q):
    print('子进程启动{}'.format(os.getpid()))
    while True:
        c = q.get()
        print(c)
    print('子进程结束{}'.format(os.getpid()))

if __name__ == '__main__':
    print('父进程启动')
    q = Queue()
    p1 = Process(target=write, args=(q,))
    p2 = Process(target=read, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.terminate()  # 强制结束进程
    print('父进程结束')
