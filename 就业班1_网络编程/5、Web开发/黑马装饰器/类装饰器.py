class Decorator(object):
    def __init__(self, func):
        print("---初始化---")
        print("函数名字是：{}".format(func.__name__))
        self.__func = func

    def __call__(self, *args, **kwargs):
        """t=Test(),t()，实例化一个类，必须有__call__方法才可以直接调用"""
        print("---装饰器功能---")
        self.__func()


@Decorator  # <==>test = Decorator(test)
def test():
    print("---test---")


if __name__ == '__main__':
    test()
