import pymysql

# db = pymysql.connect('localhost', 'root', '2017916', 'daguo')
db = pymysql.connect('192.168.21.29', 'root', '2017916', 'daguo')
cursor = db.cursor()

# 检查表是否存在，如果存在则删除
cursor.execute('drop table if exists guojiang')
# 建表
sql = 'create table guojiang(id int auto_increment primary key,name varchar(20) not null)'
# cursor.execute(sql)
print(sql[10])

cursor.close()
db.close()
