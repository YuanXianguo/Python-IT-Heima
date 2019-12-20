class A():
    def __init__(self, v):
        self.v = v


class B():
    def __init__(self):
        self.a = A(5)

    def main(self, x, v):
        self.info()
        x = 0
        self.a.v = 0
        self.info()

    def info(self):
        print(x, self.a.v)


if __name__ == '__main__':
    x = 3
    b = B()
    b.main(0, 0)
