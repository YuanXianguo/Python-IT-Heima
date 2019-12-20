from flask_script import Manager
from app import app
from db_script import db_manager

manager = Manager(app)

@manager.command
def runserver():
    print('服务器启动！')

manager.add_command('db', db_manager)

if __name__ == '__main__':
    manager.run()

