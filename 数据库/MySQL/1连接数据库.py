import pymysql

# 参数：mysql服务所在主机IP，用户名，密码，要连接的数据库名
db = pymysql.connect('192.168.21.29', 'root', '2017916', 'news')
# db = pymysql.connect('localhost', 'root', '2017916', 'news')

# 创建一个cursor对象
cursor = db.cursor()

# 执行sql语句
sql = 'select version()'
cursor.execute(sql)

# 获取返回的信息
data = cursor.fetchone()
print(data)

# 断开连接
cursor.close()
db.close()
