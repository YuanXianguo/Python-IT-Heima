from functools import wraps


def memo(func):
    cache_d = {}  # 记录已经计算过的结果

    @wraps(func)
    def d_feibo(*args):
        if args not in cache_d:  # 如果f(n)不在备忘录里
            cache_d[args] = func(*args)
        return cache_d[args]
    return d_feibo


@memo
def feibo(n):
    if n < 3:  # f(1)=1,f(2)=1
        return 1
    return feibo(n-1) + feibo(n-2)


if __name__ == '__main__':
    for i in range(10):
        print(feibo(i+1), end=" ")
