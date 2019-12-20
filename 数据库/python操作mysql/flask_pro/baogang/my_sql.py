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
    mysql = PyMySQL("localhost", 3306, "root", "pwd", "baogang")

    # mysql.delete("delete from pictures", ())
    print(len(mysql.get_all("select * from pictures", ())))
