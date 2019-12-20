import pymysql


class MySQL(object):
    """python操作mysql类"""
    def __init__(self, ip, user, passwd, db_name):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.db_name = db_name

    def connect(self):
        """连接数据库"""
        self.db = pymysql.connect(self.ip, self.user, self.passwd, self.db_name)
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
