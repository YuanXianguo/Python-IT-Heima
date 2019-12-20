from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)


class Config(object):
    # 配置参数
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:2017916@127.0.0.1:3306/db_python"
    # 设置自动更新跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)

# 创建数据库工具对象
db = SQLAlchemy(app)

# 创建flask脚本管理工具对象
manager = Manager(app)

# 创建数据库迁移工具对象
Migrate(app, db)

# 向manager对象中添加数据库的操作命令
manager.add_command("db", MigrateCommand)

# 表名的常见规范
# 数据库名缩写_表名：ihome -> ih_user
# tbl_表名：tbl_user


class Role(db.Model):
    __tablename__ = "tbl_roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    users = db.relationship("User", backref="role")


class User(db.Model):
    __tablename__ = "tbl_users"

    id = db.Column(db.Integer, primary_key=True)  # 整型主键默认自增
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id"))


if __name__ == '__main__':
    # 清除数据库里的所有数据
    # db.drop_all()

    # 创建所有的表
    # db.create_all()

    # 创建对象
    # role1 = Role(name="admin")
    # # session记录对象任务
    # db.session.add(role1)
    # # 提交任务到数据库中
    # db.session.commit()
    #
    # role2 = Role(name="stuff")
    # db.session.add(role2)
    # db.session.commit()
    #
    # use1 = User(name="wang", email="wang@qq.com", password="123456", role_id=role1.id)
    # use2 = User(name="zhang", email="zhang@qq.com", password="123456", role_id=role2.id)
    # use3 = User(name="chen", email="chen@qq.com", password="123456", role_id=role2.id)
    # use4 = User(name="zhou", email="zhou@qq.com", password="123456", role_id=role1.id)
    #
    # # 一次保存多条数据
    # db.session.add_all([use1, use2, use3, use4])
    # db.session.commit()

    # 通过manager对象启动程序
    manager.run()


