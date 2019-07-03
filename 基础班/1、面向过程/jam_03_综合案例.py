class Game(object):

    top_score = 0  # 类属性记录游戏历史最高分

    @staticmethod
    def show_help():
        """静态方法显示游戏帮助信息"""
        print("帮助信息。。。")

    @classmethod
    def show_top_score(cls):
        """类方法显示历史最高分"""
        print("历史最高分：{}".format(cls.top_score))

    def __init__(self, name):
        self.name = name

    def start_game(self):
        print("{}开始游戏".format(self.name))


Game.show_help()
Game.show_top_score()

game = Game("daguo")
game.start_game()

