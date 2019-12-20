"""连接数据库格式：dialect+driver://<username>:<password>@<host>/dbname[?<options>]"""
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '2017916'
HOST = '127.0.0.1'
DATABASE = 'db_manytomany'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, DATABASE)
