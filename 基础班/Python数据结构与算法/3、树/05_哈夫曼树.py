from 堆 import HeapPreQueue


class Node(object):
    def __init__(self, weight=0):
        self.weight = weight
        self.left = None
        self.right = None

    def res(self):
        return (self.weight, (self.left, self.right))


def huffman(lst):
    node = Node()
    heap = HeapPreQueue(lst)
    i = 0
    while i < len(lst):
        node.left = heap.dequeue()
        node.right = heap.dequeue()
        node.weight = node.left[0] + node.right[0]
        print(node.res())
        heap.enqueue(node.res())
        i += 1
    return heap.dequeue()


if __name__ == '__main__':
    lst = [(3, 'a'), (2, 'b'), (1, 'c'), (4, 'd')]
    print(huffman(lst))
