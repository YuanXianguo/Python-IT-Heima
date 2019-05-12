import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率的常量
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name="./images/background.png", speed=1):
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed


class BackGround(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):

        super().__init__()

        # 判断是否是替换图像，如果是，将初始位置设置在屏幕上方
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 调用父类的方法
        super().update()

        # 判断是否移出屏幕，如果移出，将图形设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """敌机"""

    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.speed = random.randint(1, 3)
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()

        # 判断敌机是否飞出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            # 将精灵从所有组中删除
            self.kill()


class Hero(GameSprite):

    def __init__(self):
        super().__init__("./images/me1.png", 0)

        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.rect.centerx = SCREEN_RECT.centerx

        # 创建空的子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):

        self.rect.x += self.speed

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width

    def fire(self):

        # 创建子弹精灵
        for i in range(3):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx

            # 将子弹精灵添加到子弹精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):

    def __init__(self):
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


