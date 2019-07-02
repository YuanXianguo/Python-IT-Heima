from collections import defaultdict


def cnk(n, k):
    dd = defaultdict(int)
    for i in range(n+1):
        for j in range(k+1):
            if j == 0:
                dd[i, j] = 1
            elif i == 0:
                dd[i, j] = 0
            else:
                dd[i, j] = dd[i-1, j-1] + dd[i-1, j]
        print(dd)
    return dd[n, k]


if __name__ == '__main__':
    print(cnk(4, 2))
