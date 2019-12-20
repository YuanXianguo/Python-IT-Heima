import threading


# 创建全局local对象
thread_local = threading.local()


def process_student():
    # 获取当前线程关联的student
    std = thread_local.student
    print("hello, {} in {}".format(std, threading.current_thread().name))


def process_thread(name):
    # 绑定thread_local的student
    thread_local.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=("小明", ), name="Thread-A")
t2 = threading.Thread(target=process_thread, args=("小花",), name="Thread-B")
t1.start()
t2.start()
t1.join()
t2.join()

