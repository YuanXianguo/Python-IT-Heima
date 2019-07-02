def merge_sort(alist):
    """归并排序"""

    n = len(alist)
    if n <= 1:  # 拆分到只剩1个单元结束，可以为空列表
        return alist

    mid = n // 2
    # left采用归并排序后形成的有序的新的列表
    left_list = merge_sort(alist[:mid])
    # right采用归并排序后形成的有序的新的列表
    right_list = merge_sort(alist[mid:])

    # 将两个有序的子序列合并为一个新的整体
    left_p, right_p = 0, 0
    res_list = []
    while left_p < len(left_list) and right_p < len(right_list):
        if left_list[left_p] <= right_list[right_p]:
            res_list.append(left_list[left_p])
            left_p += 1
        else:
            res_list.append(right_list[right_p])
            right_p += 1
    res_list.extend(left_list[left_p:])
    res_list.extend(right_list[right_p:])
    return res_list


if __name__ == '__main__':
   print(merge_sort([10-i for i in range(10)]))
