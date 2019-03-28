def fei_bo(num):
    a, b = 0, 1
    count = 0
    while count < num:
        yield a
        a, b = b, a+b
        count += 1


if __name__ == '__main__':
    for i in fei_bo(10):
        print(i)
