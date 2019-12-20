from 封装进程 import MyProcess

if __name__ == '__main__':
    print('父进程启动')
    p = MyProcess('test')
    p.start()
    p.join()
    print('父进程结束')
