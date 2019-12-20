class ModelMetalClass(type):
    def __new__(cls, name, bases, attrs):
        # 判断是否需要保存
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, tuple):
                mappings[k] = v

        # 删除已经在字典种保存的属性
        for k in mappings.keys():
            attrs.pop(k)

        # 将新建的字典和类名添加到属性中
        attrs["__mappings__"] = mappings
        attrs["__table__"] = name
        # return type(name, bases, attrs)
        return type.__new__(cls, name, bases, attrs)


class Model(object, metaclass=ModelMetalClass):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def inert(self):
        fields = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v[0])
            args.append(getattr(self, k, None))

        args_temp = []
        for arg in args:
            if isinstance(arg, int):
                args_temp.append(str(arg))
            elif isinstance(arg, str):
                args_temp.append("""'%s'""" % arg)
        sql = "insert into %s (%s) values (%s)" % (self.__table__, ",".join(fields), ",".join(args_temp))
        print(sql)


class User(Model):
    uid = ("uid", "itn unsigned")
    name = ("username", "varchar(30)")
    email = ("email", "varchar(30)")
    password = ("password", "varchar(30)")


user = User(uid=2019, name="daguo", email="123@qq.com", password=123456)
user.inert()
