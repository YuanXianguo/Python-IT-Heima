from greenlet import greenlet
import time


def my_gl1():
    while True:
        print("---A---")
        g2.switch()
        time.sleep(1)


def my_gl2():
    while True:
        print("---B---")
        g1.switch()
        time.sleep(1)


g1 = greenlet(my_gl1)
g2 = greenlet(my_gl2)

# 切换到g1中运行
g1.switch()
