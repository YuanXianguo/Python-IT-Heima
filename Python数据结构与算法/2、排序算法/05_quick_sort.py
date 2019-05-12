def quick_sort(alist, first, last):
    """快速排序"""
    if first >= last:
        return
    mid_value = alist[first]  # 基准
    low = first
    high = last
    while low < high:
        # high左移
        while low < high and mid_value <= alist[high]:
            high -= 1
        alist[low] = alist[high]
        # low右移
        while low < high and mid_value > alist[low]:
            low += 1
        alist[high] = alist[low]
    alist[low] = mid_value
    # 对low左边递归排序
    quick_sort(alist, first, low-1)
    # 对low右边递归排序
    quick_sort(alist, low+1, last)


if __name__ == '__main__':
    li = [10-i for i in range(10)]
    print(li)
    quick_sort(li, 0, len(li)-1)
    print(li)
