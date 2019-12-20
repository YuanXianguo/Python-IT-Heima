from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker

# 连接 mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
engine = create_engine('mysql+pymysql://root:2017916@localhost/heima?charset=utf8')

# 声明映像
Base = declarative_base()

# 创建会话
Session = sessionmaker(bind=engine)


class News(Base):
    """声明模型"""
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000))
    created_at = Column(DateTime)
    types = Column(String(20), nullable=False)
    images = Column(String(200), nullable=False)
    author = Column(String(20))
    view_count = Column(Integer)
    is_valid = Column(Boolean)

    def __repr__(self):
        pass


News.metadata.create_all(engine)


class Crud():
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
        return self.session.query(News).filter_by(is_valid=1)

    def update_data(self, id):
        """修改单条数据"""
        obj = self.session.query(News).get(id)
        if obj:
            obj.is_valid = 0
            self.session.add(obj)
            self.session.commit()
            return obj
        return False

    def update_datas(self, id):
        """修改多条数据"""
        data_list = self.session.query(News).filter(id>5)
        for data in data_list:
            data.is_valid = 0
            self.session.add(data)
        self.session.commit()

    def delete_data(self, id):
        """删除数据"""
        data = self.session.query(News).get(id)
        self.session.delete(data)
        self.session.commit()


# def crud_main():
#     crud = Crud()
#     return crud

if __name__ == '__main__':
    # res = crud_main().get_more()
    # for i in res:
    #     print(i.id)
    c = Crud()
    c.add_one()
