class Node(object):
    """单链表的结点"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None


class SingleCycleLinkList(object):
    """单向循环链表"""

    def __init__(self, node=None):
        self.__head = node
        if node:
            node.next = node

    def is_empty(self):
        return self.__head is None

    def length(self):
        if self.is_empty():
            return 0
        cursor = self.__head
        count = 1
        while cursor.next != self.__head:
            count += 1
            cursor = cursor.next
        return count

    def travel(self):
        if self.is_empty():
            return
        cursor = self.__head
        while cursor.next != self.__head:
            print(cursor.elem, end=" ")
            cursor = cursor.next
        # 退出循环游标指向尾结点，但未打印
        print(cursor.elem)

    def add(self, item):
        node = Node(item)
        if self.is_empty():
            self.__head = node
            node.next = node
        else:
            cursor = self.__head
            while cursor.next != self.__head:
                cursor = cursor.next
            cursor.next = node
            node.next = self.__head
            self.__head = node

    def append(self, item):
        node = Node(item)
        if self.is_empty():
            self.__head = node
            node.next = node
        else:
            cursor = self.__head
            while cursor.next != self.__head:
                cursor = cursor.next
            cursor.next = node
            node.next = self.__head

    def insert(self, pos, item):
        if pos <= 0:
            self.add(item)
        elif pos >= self.length():
            self.append(item)
        else:
            pre = self.__head
            count = 0  # count可以理解为当前游标位置
            while count < pos - 1:
                count += 1
                pre = pre.next
            node = Node(item)
            node.next = pre.next
            pre.next = node

    def remove(self, item):
        if self.is_empty():
            return
        cursor = self.__head
        pre = None
        while cursor.next != self.__head:
            if cursor.elem == item:
                if cursor == self.__head:
                    rear = self.__head
                    while rear.next != self.__head:
                        rear = rear.next
                    self.__head = cursor.next
                    rear.next = self.__head
                else:
                    pre.next = cursor.next
                return
            else:
                pre = cursor
                cursor = cursor.next
        # 删除尾结点
        if cursor.elem == item:
            if cursor == self.__head:
                self.__head = None
            else:
                pre.next = cursor.next

    def search(self, item):
        if self.is_empty():
            return False
        cursor = self.__head
        while cursor.next != self.__head:
            if cursor.elem == item:
                return True
            else:
                cursor = cursor.next
        if cursor.elem == item:  # 游标指向尾结点，但未判断
            return True
        else:
            return False


def main():
    scll = SingleCycleLinkList()
    scll.append(1)
    scll.append(2)
    scll.append(3)
    print(scll.is_empty())
    print(scll.length())
    scll.travel()
    scll.add(10)
    scll.append(100)
    scll.insert(3, 1000)
    scll.travel()
    scll.remove(10)
    print(scll.search(10))
    print(scll.search(1000))
    scll.travel()


if __name__ == '__main__':
    main()

