import types


class Test(object):

    __slots__ = ("name", "run")  # 限制动态添加属性范围

    def __init__(self):
        self.name = "test"


def run(self):
    print("{}---run---".format(self.name))


def t1():
    t = Test()
    t.run = run
    t.run(t)


def t2():
    t = Test()
    t.run = types.MethodType(run, t)
    t.run()


if __name__ == '__main__':
    t1()
    t2()


