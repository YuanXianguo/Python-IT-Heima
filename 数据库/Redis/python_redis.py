import redis


class MyRedis(object):
    """redis封装类"""
    def __init__(self, password, host="localhost", port=6379):
        self.__redis = redis.StrictRedis(host=host, port=port, password=password)

    def set(self, key, value):
        self.__redis.set(key, value)

    def get(self, key):
        if self.__redis.exists(key):
            return self.__redis.get(key)
        else:
            return ""

    def get_all(self):
        return self.__redis.keys()

    def delete(self, *args):
        for i in args:
            self.__redis.delete(i)


if __name__ == '__main__':
    myredis = MyRedis("2017916yuan")
    print(myredis.get("p1"))
    res = myredis.get_all()
    myredis.delete(*res)
    print(myredis.get_all())
