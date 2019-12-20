from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import Article


# 要使用flask_migrate，必须绑定app和db
migrate = Migrate(app, db)

# 把MigrateCommand命令添加到manager中
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
