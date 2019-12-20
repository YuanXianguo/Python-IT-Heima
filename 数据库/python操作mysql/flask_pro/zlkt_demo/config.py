import os

DEBUG = True

SECRET_KEY = os.urandom(24)

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '2017916'
HOST = '127.0.0.1'
DATABASE = 'zlkt_demo'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
VARIABLE_VALUE = False
