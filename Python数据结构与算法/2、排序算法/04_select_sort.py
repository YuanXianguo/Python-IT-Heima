def select_sort(alist):
    """选择排序"""
    n = len(alist)
    for j in range(n - 1):  # 假定第j个数字最小（前面已经有序）
        min_index = j
        for i in range(j+1, n):  # 从j+1开始依次比较
            if alist[i] < alist[min_index]:
                min_index = i
        alist[j], alist[min_index] = alist[min_index], alist[j]
    return alist


if __name__ == '__main__':
    print(select_sort([2,3,5,1,4]))
