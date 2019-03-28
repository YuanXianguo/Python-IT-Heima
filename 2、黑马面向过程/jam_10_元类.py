def run(self):
    print("{}会跑".format(self.name))


# type称为元类，可以创建类，参数：类名，父类（元组），属性（字典）
# 可以在用属性引用一个函数作为方法
Test = type("Test", (object,), {"name": "test", "run": run})

t = Test()
t.run()

