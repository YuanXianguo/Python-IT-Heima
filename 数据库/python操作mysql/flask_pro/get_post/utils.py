from flask import g

def login_log():
    print('用户名：{}'.format(g.username))
