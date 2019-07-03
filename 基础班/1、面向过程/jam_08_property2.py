class Test(object):
    def __init__(self):
        self.__num = 100

    @property
    def num(self):
        print("---getter---")
        return self.__num

    @num.setter
    def num(self, value):
        print("---setter---")
        if 0 < value < 100:
            self.__num = value
        else:
            self.__num = 0


if __name__ == '__main__':
    test = Test()
    print(test.num)  # <==> print(test.get_num())
    test.num = 200  # <==> print(test.set_num(200))
    print(test.num)

