class MusicPlayer(object):

    instance = None  # 记录第一被创建对象的引用
    init_flag = False  # 判断是否执行过初始化动作

    def __new__(cls, *args, **kwargs):

        # 如果还没有创建一个对象，调用父类方法，为第一个对象分配空间
        if not cls.instance:
            cls.instance = super().__new__(cls)

        # 返回类属性保存的对象引用
        return cls.instance

    def __init__(self):
        """让初始化动作只执行一次"""

        if not self.init_flag:
            print("播放器初始化")
            self.init_flag = True


player1 = MusicPlayer()
print(player1)

player2 = MusicPlayer()
print(player2)
