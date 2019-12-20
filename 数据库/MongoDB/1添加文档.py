from pymongo import MongoClient


# 连接服务器
conn = MongoClient("localhost", 27017)

# 连接数据库
db = conn.mydb

# 获取集合
collection = db.student

# 添加文档
collection.insert({
    "name": "guojiang",
    "age":  18,
    "gender": 1,
    "address": "河南",
    "isDelete": 0
})

# 添加多个文档
collection.insert([
    {
        "name": "guojiang2",
        "age":  19,
        "gender": 1,
        "address": "河南",
        "isDelete": 0
    },
    {
        "name": "guojiang3",
        "age": 20,
        "gender": 1,
        "address": "河南",
        "isDelete": 0
    }
])

# 断开
conn.close()
