import pymysql

# db = pymysql.connect('localhost', 'root', '2017916', 'daguo')
db = pymysql.connect('192.168.21.29', 'root', '2017916', 'daguo')
cursor = db.cursor()

sql = "update guojiang set name='python' where id=1"
try:
    cursor.execute(sql)
    db.commit()  # 提交数据
except:  # 如果提交失败，回滚到上一次数据
    db.rollback()

cursor.close()
db.close()
