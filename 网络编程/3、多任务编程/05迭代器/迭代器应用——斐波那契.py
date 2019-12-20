class FeiBo(object):

    def __init__(self, num):
        self.num = num
        self.count = -1  # 计数
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count:  # 第一次直接返回self.a
            self.a, self.b = self.b, self.a + self.b
        if self.count < self.num:
            return self.a
        else:
            raise StopIteration


def main():
    fei = FeiBo(10)
    for f in fei:
        print(f)


if __name__ == '__main__':
    main()


