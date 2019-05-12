import heapq


class HeapPreQueue(object):
    """优先队列——堆"""
    def __init__(self, heap_lst):
        self.heap = heap_lst
        heapq.heapify(self.heap)  # 使用列表创建最小堆

    def enqueue(self, elem):
        """向最小堆添加元素"""
        heapq.heappush(self.heap, elem)

    def dequeue(self):
        """弹出最小堆中的最小值"""
        return heapq.heappop(self.heap)


def heapq_else_use():
    """堆其他用法"""
    # 合并多个排序后的序列成一个排序后的序列，返回值为迭代器
    num1 = [32, 3, 5, 54]
    num2 = [23, 2, 12, 65]
    res = heapq.merge(sorted(num1), sorted(num2))
    print(list(res))

    # 获取最大或做小范围值
    nums = [1, 3, 4, 5, 2]
    print(heapq.nlargest(3, nums))
    print(heapq.nsmallest(3, nums))

    # 获取dict或其他数据结构类型的最大后最小范围值
    portfolio = [
        {'name': 'IBM', 'shares': 100, 'price': 91.1},
        {'name': 'AAPL', 'shares': 50, 'price': 543.22},
        {'name': 'FB', 'shares': 200, 'price': 21.09},
        {'name': 'HPQ', 'shares': 35, 'price': 31.75},
        {'name': 'YHOO', 'shares': 45, 'price': 16.35},
        {'name': 'ACME', 'shares': 75, 'price': 115.65}]
    cheap = heapq.nsmallest(3, portfolio, key=lambda s: s["price"])
    exp = heapq.nlargest(3, portfolio, key=lambda s: s["price"])
    print(cheap)
    print(exp)


def heap_sort(lst):
    """实现heap堆排序算法"""

    heapq.heapify(lst)
    return [heapq.heappop(lst) for i in range(len(lst))]


def main():
    lst = []
    h = HeapPreQueue(lst)
    print(h.heap)

    lst = list(range(10))
    heap = HeapPreQueue(lst)
    heap.enqueue(-1)
    print(heap.heap)
    print(heap.dequeue())


if __name__ == '__main__':
    main()
    print(heap_sort([3, 5, 2, 7, 1]))
    heapq_else_use()



