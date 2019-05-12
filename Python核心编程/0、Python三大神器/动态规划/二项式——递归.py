"""二项式C(n,k)表示从n个中选k个，假设我们现在处理n个中的第1个，考虑是否选择它：
如果选择它的话，那么我们还需要从剩下的n-1个中选k-1个，即C(n-1,k-1)；
如果不选择它的话，我们需要从剩下的n-1中选k个，即C(n-1,k)。
所以，C(n,k)=C(n-1,k-1)+C(n-1,k)"""
from functools import wraps


def memo(func):
    cache_d = {}

    @wraps(func)
    def inner(*args):
        print(cache_d)
        if args not in cache_d:
            cache_d[args] = func(*args)
        return cache_d[args]
    return inner


@memo
def cnk(n, k):
    if k == 0:
        return 1
    if n == 0:
        return 0
    return cnk(n-1, k-1) + cnk(n-1, k)


if __name__ == '__main__':
    print(cnk(4, 2))
