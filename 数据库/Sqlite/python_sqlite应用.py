from python_sqlite import MySqlite


if __name__ == '__main__':
    db = "E:/Sqlite/test1.db"
    sqlite = MySqlite(db)
    sqlite.drop_table("student")

    sqlite.create_table("create table student(" 
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, " 
                        "name varchar(20) not null, " 
                        "gender bit default(1), " 
                        "age int not null, " 
                        "address varchar(100))")

    sqlite.insert("insert into student('name', 'gender', 'age', 'address') "
                  "values('daguo', 1, 18, '杭州'),"
                  "('guojiang', 1, 19, '上海'),"
                  "('hanmeimei', 0, 18, '杭州')")
    sqlite.insert("insert into student('name', 'gender', 'age', 'address') "
                  "values('daguo', 1, 18, '杭州'),"
                  "('guojiang', 1, 19, '上海'),"
                  "('hanmeimei', 0, 18, '杭州')")
    res = sqlite.get_all("select * from student")
    print(res)
