import pymysql


class PyMySQL(object):
    def __init__(self, host, port, user, password, database, charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    def connect(self):
        self.con = pymysql.connect(host=self.host,
                                   port=self.port,
                                   user=self.user,
                                   password=self.password,
                                   database=self.database,
                                   charset=self.charset)
        self.cursor = self.con.cursor()

    def close(self):
        self.cursor.close()
        self.con.close()

    def get_one(self, sql, para):
        self.connect()
        self.cursor.execute(sql, para)
        res = self.cursor.fetchone()
        self.close()
        return res

    def get_all(self, sql, para):
        self.connect()
        self.cursor.execute(sql, para)
        res = self.cursor.fetchall()
        self.close()
        return res

    def insert(self, sql, para):
        self.execute_sql(sql, para)

    def delete(self, sql, para):
        self.execute_sql(sql, para)

    def update(self, sql, para):
        self.execute_sql(sql, para)

    def execute_sql(self, sql, para):
        self.connect()
        try:
            self.cursor.execute(sql, para)
            self.con.commit()
        except:
            self.con.rollback()
        self.close()


if __name__ == '__main__':
    mysql = PyMySQL("localhost", 3306, "root", "2017916", "stock_db")
    sql = "select * from info where code=%s;"
    stock = mysql.get_one(sql, ("000528",))
    if not stock:
        print("没有这支股票")
    # 判断下是否已经关注过
    sql = "select * from focus where info_id=%s;"
    if mysql.get_one(sql, stock[0]):
        print("已经关注过了")
    else:
        sql = "insert into focus (info_id) values (%s);"
        mysql.insert(sql, stock[0])
