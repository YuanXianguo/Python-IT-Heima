import time


def test1():
    while True:
        print("---A---")
        time.sleep(1)
        yield


def test2(a):
    while True:
        print("---B---")
        time.sleep(1)
        next(a)


if __name__ == '__main__':
    test2(test1())


