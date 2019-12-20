import threading, time

def r(num):
    # current_thread()返回当前线程的一个实例
    print('子线程{}启动'.format(threading.current_thread().name))
    time.sleep(num)
    print('子线程{}结束'.format(threading.current_thread().name))

if __name__ == '__main__':
    print('父线程{}启动'.format(threading.current_thread().name))
    t = threading.Thread(target=r, args=(1,))
    t2 = threading.Thread(target=r, args=(1,))
    t.start()
    t2.start()
    t.join()
    t2.join()
    print('父线程{}结束'.format(threading.current_thread().name))
