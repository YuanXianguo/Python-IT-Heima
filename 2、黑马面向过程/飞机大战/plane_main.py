from plane_sprites import *


class PlaneGame(object):
    """飞机大战游戏主程序"""

    def __init__(self):

        # 创建游戏的主窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        # 创建游戏的时钟
        self.clock = pygame.time.Clock()

        # 调用私有方法，创建精灵和精灵组
        self.__create_sprites()

        # 设置定时器事件：创建敌机，1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 设置定时器事件：创建英雄，0.5s
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        """创建精灵及精灵组"""

        # 创建背景精灵和背景精灵组
        bg1 = BackGround()
        bg2 = BackGround(True)

        self.bg_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        """开始游戏循环"""

        while True:
            # 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)

            # 事件监听
            self.__event_handler()

            # 碰撞检测
            self.__check_collide()

            # 更新/绘制精灵组
            self.__update_sprites()

            # 更新显示
            pygame.display.update()

    def __event_handler(self):
        """监听事件"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 使用键盘提供的方法获取键盘按键--元组
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):
        """检测碰撞"""

        # 两个精灵组中所有的精灵的碰撞检测（子弹组，敌机组），可以返回碰撞字典
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True,
                                   True)

        # 判断某个精灵和指定精灵组的碰撞（英雄，敌机组），可以返回碰撞列表
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断是否有敌机碰撞到了英雄
        if len(enemies):
            self.hero.kill()  # 英雄牺牲
            self.__game_over()  # 游戏结束

    def __update_sprites(self):
        """更新精灵组"""

        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        """结束游戏"""

        pygame.quit()
        exit()


if __name__ == '__main__':

    game = PlaneGame()
    game.start_game()



