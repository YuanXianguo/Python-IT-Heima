from multiprocessing import Pool
import time
import os


def test():
    print("---进程池中的进程---pid={},ppid={}".format(os.getpid(), os.getppid()))
    for i in range(3):
        print("---{}---".format(i))
        time.sleep(1)
    return "哈哈哈"


def test2(args):
    print("---callback func---pid={}".format(os.getpid()))
    # callback会将子进程返回的值传给主进程
    print("---callback func---args={}".format(args))


if __name__ == '__main__':
    pool = Pool(3)
    pool.apply_async(func=test, callback=test2)

    time.sleep(5)

    print("---主进程-pid={}".format(os.getpid()))
