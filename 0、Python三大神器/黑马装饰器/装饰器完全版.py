def decorator(char):
    def decorator_(func):
        def inner(*args, **kwargs):
            print(char * 50)
            res = func(*args, **kwargs)
            return res
        return inner
    return decorator_


@decorator("*")
def test(a, b, c=3):
    return a + b + c


if __name__ == '__main__':
    print(test(1, 2, 4))

