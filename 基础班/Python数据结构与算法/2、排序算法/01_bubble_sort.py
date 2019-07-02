def bubble_sort(alist):
    """冒泡排序"""
    n = len(alist)
    for i in range(n-1, 0, -1):  # 每一趟需要比较的最后一个数索引
        flag = 1
        for j in range(i):
            if alist[j] > alist[j+1]:  # 逐次比较相邻两个
                alist[j], alist[j+1] = alist[j+1], alist[j]
                flag = 0
        if flag:
            return alist
    return alist


if __name__ == '__main__':
    print(bubble_sort([3,6,7,8,1,2,5]))
