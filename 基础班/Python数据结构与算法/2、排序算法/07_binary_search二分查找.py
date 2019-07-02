def binary_search(alist, item):
    """二分查找"""
    n = len(alist)
    if n:
        mid = n // 2
        if item == alist[mid]:
            return True
        elif item < alist[mid]:
            binary_search(alist[:mid], item)
        else:
            binary_search(alist[mid+1:], item)
    return False


def binary_search2(alist, item):
    """二分查找，非递归"""
    n = len(alist)
    first = 0
    last = n - 1
    while first <= last:
        mid = (first + last) // 2
        if item == alist[mid]:
            return True
        elif item < alist[mid]:
            last = mid - 1
        else:
            first = mid + 1
    return False


if __name__ == '__main__':
    print(binary_search([i for i in range(10)], 11))
    print(binary_search2([i for i in range(10)], 11))

