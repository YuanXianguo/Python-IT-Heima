def fei_bo(num):
    a, b = 1, 1
    while num:
        yield a
        a, b = b, a+b
        num -= 1


def fei_bo_iter(num):
    a, b = 1, 1
    count = 0
    while count < num:
        yield a
        a, b = b, a+b
        count += 1


if __name__ == '__main__':
    for i in fei_bo(10):
        print(i, end=" ")
    print("")
    for i in fei_bo_iter(10):
        print(i, end=" ")
    print("")
