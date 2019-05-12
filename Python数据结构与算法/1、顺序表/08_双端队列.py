class DoubleQueue(object):
    """双端队列"""
    def __init__(self):
        self.__list = []

    def is_empty(self):
        return not self.__list

    def size(self):
        return len(self.__list)

    def add_rear(self, item):
        self.__list.append(item)

    def add_front(self, item):
        self.__list.insert(0, item)

    def pop_front(self):
        if self.is_empty():
            return None
        return self.__list.pop(0)

    def pop_rear(self):
        if self.is_empty():
            return None
        return self.__list.pop()
