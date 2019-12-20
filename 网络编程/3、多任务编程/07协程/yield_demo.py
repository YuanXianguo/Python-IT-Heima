import time


def my_yield1():
    while True:
        print("---A---")
        time.sleep(1)
        yield


def my_yield2():
    while True:
        print("---B---")
        time.sleep(1)
        yield


def main():
    while True:
        next(my_yield1())
        next(my_yield2())


if __name__ == '__main__':
    main()

