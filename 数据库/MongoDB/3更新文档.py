from pymongo import MongoClient


conn = MongoClient("localhost", 27017)

db = conn.mydb

collection = db.student

# 更新文档
collection.update({"name": "lilei"}, {"$set": {"age": 25}})

# 删除
collection.remove({"name": "guojiang3"})

# 断开
conn.close()
