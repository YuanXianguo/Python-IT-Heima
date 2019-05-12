class Queue(object):
    """队列"""
    def __init__(self):
        self.__list = []

    def is_empty(self):
        return not self.__list

    def size(self):
        return len(self.__list)

    def enqueue(self, item):
        self.__list.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.__list.pop(0)


if __name__ == '__main__':
    q = Queue()
    for i in range(4):
        q.enqueue(i)
    print(q.is_empty())
    print(q.size())
    for i in range(5):
        print(q.dequeue())
