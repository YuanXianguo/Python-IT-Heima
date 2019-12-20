class IteratorDemo(object):
    """迭代器，可迭代对象"""

    def __init__(self):
        self.li = [i for i in range(10)]
        self.count = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count < len(self.li):
            return self.li[self.count]
        else:
            raise StopIteration  # 表示迭代器值取完


def main():
    iter_demo = IteratorDemo()
    for i in iter_demo:
        print(i)


if __name__ == '__main__':
    main()
