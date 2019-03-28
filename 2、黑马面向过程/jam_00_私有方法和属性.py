class Test(object):
    def __init__(self):
        self.__num = 100

    def __hello(self):
        print("hello!")

    def get_num(self):
        print(self.__num)

    def get_hello(self):
        self.__hello()


if __name__ == '__main__':
    test = Test()
    test.get_hello()
    test.get_num()
