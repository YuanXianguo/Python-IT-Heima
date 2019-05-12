def shell_sort(alist):
    """希尔排序"""
    n = len(alist)
    gap = n // 2
    while gap:  # 控制步长
        # 内部与插入算法的区别就是gap步长
        for i in range(gap, n):
            tmp = alist[i]
            while i >= gap and alist[i-gap] > tmp:
                alist[i] = alist[i-gap]
                i -= gap
            alist[i] = tmp
        gap //= 2
    return alist


if __name__ == '__main__':
    print(shell_sort([3,6,1,3,4,8,3,11,10,100,1,12]))
