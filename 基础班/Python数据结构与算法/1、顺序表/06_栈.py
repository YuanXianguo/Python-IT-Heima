class Stack(object):
    """栈"""
    def __init__(self):
        self.__list = []

    def is_empty(self):
        return not self.__list

    def size(self):
        return len(self.__list)

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.__list.pop()

    def peek(self):
        """返回栈顶元素"""
        if self.is_empty():
            return None
        return self.__list[-1]


if __name__ == '__main__':
    s = Stack()
    for i in range(4):
        s.push(i)
    print(s.size())
    for i in range(5):
        print(s.pop())
