class IterableDemo(object):
    """可迭代对象类"""

    def __init__(self):
        self.li = [i for i in range(10)]

    def __iter__(self):
        return IteratorDemo(self)


class IteratorDemo(object):
    """迭代器类"""

    def __init__(self, obj):
        self.obj = obj
        self.count = -1

    def __iter__(self):
        pass

    def __next__(self):
        self.count += 1
        if self.count < len(self.obj.li):
            return self.obj.li[self.count]
        else:
            raise StopIteration  # 表示迭代器值取完


def main():
    iter_demo = IterableDemo()
    for i in iter_demo:
        print(i)


if __name__ == '__main__':
    main()
