def test1(func):
    print("---装饰器1---")

    def inner1():
        print("---正在验证1---")
        func()
    return inner1


def test2(func):
    print("---装饰器2---")

    def inner2():
        print("---正在验证2---")
        func()
    return inner2


# 装饰器在@符号之后就自动的进行装饰，而不是等到调用的时候
@test1  # test = test1(test)，参数为inner2，指向后test指向inner1
@test2  # test = test2(test)，参数为test，执行后test指向inner2
def test():
    print("---test---")


if __name__ == '__main__':
    test()


