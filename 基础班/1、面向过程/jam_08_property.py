class Test(object):
    def __init__(self):
        self.__num = 100

    def get_num(self):
        print("---getter---")
        return self.__num

    def set_num(self, value):
        print("---setter---")
        self.__num = value

    num = property(get_num, set_num)


if __name__ == '__main__':
    test = Test()
    print(test.num)  # <==> print(test.get_num())
    test.num = 200  # <==> print(test.set_num(200))
    print(test.num)

