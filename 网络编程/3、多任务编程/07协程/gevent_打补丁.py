from gevent import monkey
import gevent
import time

# 处理耗时操作
monkey.patch_all()


def my_ge(n):
    for i in range(n):
        print(gevent.getcurrent(), i)
        time.sleep(1)


gevent.joinall([
    gevent.spawn(my_ge, 5),
    gevent.spawn(my_ge, 5),
])
