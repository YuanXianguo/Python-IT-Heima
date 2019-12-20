import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId  # 用于id查询


conn = MongoClient("localhost", 27017)
db = conn.mydb
collection = db.student

# 查询所有文档
res = collection.find()
for row in res:
    print(row)

# 条件查询，年龄大于18
res = collection.find({"age": {"$gt": 18}})
for row in res:
    print(row)

# 查询统计
res = collection.find({"age": {"$gt": 18}}).count()
print(res)

# 排序，默认升序，按年龄
res = collection.find({"age": {"$gt": 18}}).sort("age")
for row in res:
    print(row)

# 降序排序
res = collection.find({"age": {"$gt": 18}}).sort("age", pymongo.DESCENDING)
for row in res:
    print(row)

# 根据id查询
res = collection.find({"_id": ObjectId("5ca41ede4e24d1224856c408")})
print(res[0])

# 分页查询
res = collection.find().skip(2).limit(2)
for row in res:
    print(row)

conn.close()

