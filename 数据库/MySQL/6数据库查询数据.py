import pymysql

# db = pymysql.connect('localhost', 'root', '2017916', 'daguo')
db = pymysql.connect('192.168.21.29', 'root', '2017916', 'heima')
cursor = db.cursor()

sql = "select * from student"
try:
    cursor.execute(sql)
    data_list = cursor.fetchall()
    for row in data_list:
        print(row)
        print(row[0], '', row[1])

except:  # 如果提交失败，回滚到上一次数据
    db.rollback()

cursor.close()
db.close()
