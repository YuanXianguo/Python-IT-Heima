import gevent


def test(n):
    for i in range(n):
        # 打印当前协程
        print(gevent.getcurrent, i)

        # 用来模拟一个耗时操作，注意不是time模块种的sleep
        gevent.sleep(1)


g1 = gevent.spawn(test, 5)
g2 = gevent.spawn(test, 5)
# 等待协程结束
g1.join()
g2.join()

