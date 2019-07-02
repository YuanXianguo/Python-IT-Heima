class Node(object):
    """双向链表的结点"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None
        self.prev = None


class DoubleLinkList(object):
    """双向链表"""
    def __init__(self, node=None):
        self.__head = node

    def is_empty(self):
        return self.__head is None

    def length(self):
        cursor = self.__head
        count = 0
        while cursor:
            count += 1
            cursor = cursor.next
        return count

    def travel(self):
        cursor = self.__head
        while cursor:
            print(cursor.elem, end=" ")
            cursor = cursor.next
        print("")

    def add(self, item):
        node = Node(item)
        node.next = self.__head
        self.__head.prev = node
        self.__head = node

    def append(self, item):
        node = Node(item)
        if self.is_empty():
            self.__head = node
        else:
            cursor = self.__head
            while cursor.next:
                cursor = cursor.next
            cursor.next = node
            node.prev = cursor

    def insert(self, pos, item):
        if pos <= 0:
            self.add(item)
        elif pos >= self.length():
            self.append(item)
        else:
            cursor = self.__head
            count = 0
            while count < pos:
                count += 1
                cursor = cursor.next
            node = Node(item)
            node.next = cursor
            node.prev = cursor.prev
            cursor.prev.next = node
            cursor.prev = node
            # node.prev.next = node

    def remove(self, item):
        cursor = self.__head
        while cursor:
            if cursor.elem == item:
                if cursor.elem == self.__head:
                    self.__head = cursor.next
                    if cursor.next:  # 判断链表是否只有一个结点
                        cursor.next.prev = None
                else:
                    cursor.prev.next = cursor.next
                    if cursor.next:  # 判断是否是最后一个结点
                        cursor.next.prev = cursor.prev
                break
            else:
                cursor = cursor.next

    def search(self, item):
        cursor = self.__head
        while cursor:
            if cursor.elem == item:
                return True
            else:
                cursor = cursor.next
        return False


def main():
    dll = DoubleLinkList()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    print(dll.is_empty())
    print(dll.length())
    dll.travel()
    dll.add(10)
    dll.append(100)
    dll.insert(3, 1000)
    dll.travel()
    dll.remove(2)
    print(dll.search(2))
    print(dll.search(1000))
    dll.travel()


if __name__ == '__main__':
    main()
