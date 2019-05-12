from greenlet import greenlet
import time


def test1():
    while True:
        print("---A---")
        g2.switch()
        time.sleep(1)


def test2():
    while True:
        print("---B---")
        g1.switch()
        time.sleep(1)


g1 = greenlet(test1)
g2 = greenlet(test2)

# 切换到g1中运行
g1.switch()
