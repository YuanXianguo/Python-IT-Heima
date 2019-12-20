from pymongo import MongoClient


class MyMongoDB(object):
    """mongodb类"""

    def __init__(self, db, collection, host="localhost", port=27017):
        self.db = db
        self.collection = collection
        self.host = host
        self.port = port

    def connect(self):
        """连接数据库，获得操作集合"""
        self.conn = MongoClient(self.host, self.port)  # 连接
        self.db = self.conn.get_database(self.db)  # 获得数据库
        self.collection = self.db.get_collection(self.collection)  # 获得集合

    def inset(self, *args):
        """插入文档，支持单条、多条插入"""
        self.connect()  # 连接
        doc_list = list(args)  # 将传入文档转换为列表
        self.collection.insert(doc_list)
        self.conn.close()  # 断开

    def update(self, cond_doc, set_doc, multi=False):
        """
         更新文档
        :param cond_doc: 更新文档的条件
        :param set_doc: 更新文档的内容
        :param multi：是否更新多条
        :return: None
        """
        self.connect()
        # 如果更新文档不存在，则当作新数据插入，默认只更新第一条
        self.collection.update(cond_doc, set_doc, multi=multi)
        self.conn.close()

    def remove(self, cond_doc):
        """
        删除文档
        :param cond_doc: 删除文档的条件
        :return: None
        """
        self.connect()
        self.collection.remove(cond_doc)
        self.conn.close()

    def query(self, cond_doc):
        """
        查询文档
        :param cond_doc: 查询文档的条件
        :return: 所有符合条件的文档的列表
        """
        self.connect()
        res = self.collection.find(cond_doc)
        self.conn.close()
        return res

    def find_one(self, cond_doc):
        self.connect()
        res = self.collection.find_one(cond_doc)
        self.conn.close()
        return res

    def find_many(self, cond_doc):
        self.connect()
        res = self.collection.find_many(cond_doc)
        self.conn.close()
        return res

    def update_one(self, cond_doc):
        self.connect()
        res = self.collection.update_one(cond_doc)
        self.conn.close()
        return res

    def update_many(self, cond_doc):
        self.connect()
        res = self.collection.update_many(cond_doc)
        self.conn.close()
        return res
