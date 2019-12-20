from python_mongodb import MyMongoDB


if __name__ == '__main__':
    mymongo = MyMongoDB("mydb", "student")
    doc1 = {
        "name": "guojiang4",
        "age":  19,
        "gender": 1,
        "address": "河南",
        "isDelete": 0
    }
    doc2 = {
        "name": "guojiang5",
        "age": 20,
        "gender": 1,
        "address": "河南",
        "isDelete": 0
    }
    mymongo.inset(doc1, doc2)
    mymongo.update({"name": "guojiang4"}, {"$set": {"age": 28}}, True)
    res = mymongo.query({"age": {"$lte": 18}})
    for row in res:
        print(row)
