"""根据要求构建类：print(Test().daguo.name.first_name)
->daguo name first_name"""


class Test(object):

    def __init__(self):
        self.a = "1"

    def __getattr__(self, item):
        print(item, end=" ")
        return self

    def __str__(self):
        return ""


print(Test().__dict__)
print(Test().daguo.name.first_name)
