def feibo(n):
    if n < 3:
        return 1
    a, b = 1, 1
    while n >= 2:
        a, b = b, a+b
        n -= 1
    return a


if __name__ == '__main__':
    for i in range(10):
        print(feibo(i+1), end=" ")
