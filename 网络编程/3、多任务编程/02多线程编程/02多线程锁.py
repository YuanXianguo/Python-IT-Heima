import threading

count = 100
lock = threading.Lock()

def run0(num):
    global count
    for i in range(100):
        lock.acquire()  # 加锁
        try:
            count += num
            count -= num
        finally:  # 释放锁
            lock.release()

def run(num):
    global count
    for i in range(100):
        with lock:  # 改进加锁效率
            count += num
            count -= num

if __name__ == '__main__':
    t1 = threading.Thread(target=run,args=(3,))
    t2 = threading.Thread(target=run,args=(5,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(count)


