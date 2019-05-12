class Node(object):
    """单链表的结点"""
    def __init__(self, elem):
        # item存放数据元素
        self.elem = elem
        # next是下一个结点的标识
        self.next = None


class SingleLinkList(object):
    """单链表"""

    def __init__(self, node=None):
        self.__head = node

    def is_empty(self):
        """链表是否为空"""
        return self.__head is None

    def length(self):
        """链表长度"""
        # cursor游标
        cursor = self.__head
        count = 0
        while cursor:
            count += 1
            cursor = cursor.next
        return count

    def travel(self):
        """遍历整个列表"""
        cursor = self.__head
        while cursor:
            print(cursor.elem, end=" ")
            cursor = cursor.next
        print("")

    def add(self, item):
        """链表头部添加元素，头插法"""
        node = Node(item)
        node.next = self.__head
        self.__head = node

    def append(self, item):
        """链表尾部添加元素，尾插法"""
        node = Node(item)
        if self.is_empty():
            self.__head = node
        else:
            cursor = self.__head
            while cursor.next:
                cursor = cursor.next
            cursor.next = node

    def insert(self, pos, item):
        """指定位置添加元素"""
        if pos <= 0:
            self.add(item)
        elif pos >= self.length():
            self.append(item)
        else:  # pre表示前一个结点
            pre = self.__head
            count = 0
            while count < pos - 1:
                count += 1
                pre = pre.next
            node = Node(item)
            node.next = pre.next
            pre.next = node

    def remove(self, item):
        """删除结点"""
        cursor = self.__head
        pre = None
        while cursor:
            if cursor.elem == item:
                if cursor == self.__head:
                    self.__head = cursor.next
                else:
                    pre.next = cursor.next
                break
            else:
                pre = cursor
                cursor = cursor.next

    def search(self, item):
        """查找结点"""
        cursor = self.__head
        while cursor:
            if cursor.elem == item:
                return True
            else:
                cursor = cursor.next
        return False


def main():
    sll = SingleLinkList()
    sll.append(1)
    sll.append(2)
    sll.append(3)
    print(sll.is_empty())
    print(sll.length())
    sll.travel()
    sll.add(10)
    sll.append(100)
    sll.insert(3, 1000)
    sll.travel()
    sll.remove(2)
    print(sll.search(2))
    print(sll.search(1000))
    sll.travel()


if __name__ == '__main__':
    main()

