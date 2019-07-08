class MyClass(object):
    test = 10


if __name__ == '__main__':
    if hasattr(MyClass, "test"):
        print(getattr(MyClass, "test"))
    setattr(MyClass, "test", 100)
    print(getattr(MyClass, "test"))
