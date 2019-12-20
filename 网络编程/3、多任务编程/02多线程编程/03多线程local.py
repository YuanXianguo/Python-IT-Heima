import threading

count = 100
local = threading.local()

def run(x, num):
    x += num
    x -= num

def fun(n):
    local.x = count
    for i in range(100):
        run(local.x, n)
    print(threading.current_thread().name, local.x)

if __name__ == '__main__':
    t1 = threading.Thread(target=fun,args=(3,))
    t2 = threading.Thread(target=fun,args=(5,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(count)


