from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///E:/Sqlite/test2.db?check_same_thread=False")

# 声明映像
Base = declarative_base()

# 创建会话
Session = sessionmaker(bind=engine)


class News(Base):
    """声明模型"""
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000))
    created_at = Column(DateTime)
    types = Column(String(20), nullable=False)
    images = Column(String(200), nullable=False)
    author = Column(String(20))
    view_count = Column(Integer)
    is_delete = Column(Boolean, default=0)

    def str(self):
        output = "({},{},{},{})".format(self.id, self.title, self.content, self.created_at)
        return output


# 创建数据表
News.metadata.create_all(engine)


class Crud(object):
    """操作对象，增删改查"""
    def __init__(self):
        self.session = Session()

    def add_one(self):
        """新增数据"""
        new_obj = News(title='标题', types='体育', images='abc.jpg')
        self.session.add(new_obj)
        self.session.commit()
        return new_obj

    def get_one(self):
        """获取一条数据，参数为id"""
        return self.session.query(News).get(1)

    def get_more(self):
        """获取多条数据"""
        return self.session.query(News).filter_by(is_delete=0)

    def update_data(self, id):
        """修改单条数据"""
        obj = self.session.query(News).get(id)
        if obj:
            obj.is_delete = 0
            self.session.add(obj)
            self.session.commit()
            return obj
        return False

    def update_datas(self, id):
        """修改多条数据"""
        data_list = self.session.query(News).filter(id > 5)
        for data in data_list:
            data.is_delete = 0
            self.session.add(data)
        self.session.commit()

    def delete_data(self, id):
        """删除数据"""
        data = self.session.query(News).get(id)
        self.session.delete(data)
        self.session.commit()


if __name__ == '__main__':
    c = Crud()
    res = c.get_one()
    print(res)
    print(res.str())
