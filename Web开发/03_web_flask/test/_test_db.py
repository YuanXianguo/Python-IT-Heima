import unittest
from ._03db_demo import Role, db, app


class DataBaseTest(unittest.TestCase):
    def setUp(self):
        """在进行测试前，先被执行"""
        # 设置flask工作在测试模式下
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:2017916@127.0.0.1:3306/db_python2"
        db.create_all()

    def test_add_author(self):
        """测试添加角色的数据库操作"""
        role = Role(name="da")
        db.session.add(role)
        db.session.commit()

        role_res = Role.query.filter_by(name="da").first()
        self.assertIsNotNone(role_res)

    def tearDown(self):
        """在所有的测试执行后执行，通常用来进行清理操作"""
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
