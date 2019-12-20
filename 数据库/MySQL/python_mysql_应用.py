from python_mysql import MySQL

mysql = MySQL('192.168.21.29', 'root', '2017916', 'heima')

mysql.drop_table("test")
mysql.create_table("create table test(" 
                   "id int auto_increment primary key, " 
                   "name varchar(20) not null, " 
                   "gender bit default(1), " 
                   "age int not null, " 
                   "address varchar(100))")
mysql.insert("insert into test "
             "values(0, 'daguo', 1, 18, '杭州'),"
             "(0, 'guojiang', 1, 19, '上海'),"
             "(0, 'hanmeimei', 0, 18, '杭州')")
# mysql.update("update guojiang set name='py' where id=2")
# mysql.delete("delete from guojiang where id=19")
# res = mysql.get_one("select * from {}".format("test"))
# print(res)
res_all = mysql.get_all("select * from test")
print(res_all)
