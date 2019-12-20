import redis


# 连接
r = redis.StrictRedis(host="localhost", port=6379, password="2017916yuan")

# 方法1：根据类型的不同，调用响应的方法
r.set("p1", "good")
print(r.get("p1"))

# 方法2：pipline，缓存多条命令，然后依次执行，减少服务器-客户端之间的TCP数据包
pipe = r.pipeline()
pipe.set("p2", "nice")
pipe.set("p3", "nice")
pipe.set("p4", "nice")
pipe.execute()
