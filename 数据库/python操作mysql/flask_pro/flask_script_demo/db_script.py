from flask_script import Manager

db_manager = Manager()

@db_manager.command
def init():
    print('数据库初始化完成！')

@db_manager.command
def migrate():
    print('数据表迁移成功！')
