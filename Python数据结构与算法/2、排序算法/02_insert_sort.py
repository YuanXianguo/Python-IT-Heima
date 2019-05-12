def insert_sort(alist):
    """插入排序"""
    n = len(alist)
    for i in range(1, n):  # 逐次从未排序中的第一个数开始向已有序队列插入
        tmp = alist[i]  # 临时保存当前值
        while i and alist[i-1] > tmp:  # 从有序队列后向前对比插入
            alist[i] = alist[i-1]
            i -= 1
        alist[i] = tmp
    return alist


if __name__ == '__main__':
    print(insert_sort([3,6,1,2,8,4,9,7]))
