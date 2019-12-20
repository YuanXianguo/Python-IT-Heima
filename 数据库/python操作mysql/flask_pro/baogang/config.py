import os

DEBUG = True

SECRET_KEY = os.urandom(24)  # session加密

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'pwd'
HOST = '127.0.0.1'
DATABASE = 'baogang'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

