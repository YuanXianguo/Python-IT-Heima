import sqlite3


class MySqlite(object):
    """sqlite类"""

    def __init__(self, path):
        self.path = path

    def connect(self):
        """连接数据库"""
        if self.path == ":memory:":
            self.db = sqlite3.connect(":memory:")
        else:
            self.db = sqlite3.connect(self.path)

        self.cursor = self.db.cursor()

    def close(self):
        """关闭数据库"""
        self.cursor.close()
        self.db.close()

    def drop_table(self, table):
        """删除表"""
        self.connect()
        self.cursor.execute("drop table if exists {}".format(table))
        self.close()

    def create_table(self, sql):
        """创建表"""
        return self.execute_sql(sql)

    def insert(self, sql):
        """增加数据"""
        return self.execute_sql(sql)

    def update(self, sql):
        """更新数据"""
        return self.execute_sql(sql)

    def delete(self, sql):
        """删除数据"""
        return self.execute_sql(sql)

    def execute_sql(self, sql):
        """提交事物"""
        count = 0  # 影响了多少行
        self.connect()  # 连接数据库
        try:
            count = self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            print('事务提交失败')
        self.close()  # 关闭数据库
        return count

    def get_one(self, sql):
        """fetchone查询"""
        res = ''
        self.connect()
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
        except:
            print('查询失败')
        self.close()
        return res

    def get_all(self, sql):
        """fetchall查询"""
        res = ()
        self.connect()
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except:
            print('查询失败')
        self.close()
        return res
