from threading import Thread
import time


class Client(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            t = time.localtime()
            print("1", time.strftime("%H:%M:%S", t))
            time.sleep(0.5)


class Client2(Thread):
    def run(self):
        while True:
            t = time.localtime()
            print("2", time.strftime("%H:%M:%S", t))
            time.sleep(0.5)


if __name__ == '__main__':
    c1 = Client()
    c2 = Client2()
    c1.start()
    c2.start()
