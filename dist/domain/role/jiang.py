import pygame
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT

from role import DirAction


class Jiang(pygame.sprite.Sprite):
    """
    将军角色
    """
    def __init__(self):
        """
        将军构造函数
        """
        self.huang = 0
        pygame.sprite.Sprite.__init__(self)
        self.walk = DirAction("wo", "0789-4ee87ee9-", 4, 8, True)
        self.pos_x = 30
        self.pos_y = 50
        self.hp = 100
        self.dir = 0
        self.step = 30
        self.rect = pygame.Rect(self.pos_x + 65, self.pos_y + 58, 20, 20)

    def reset_pos(self, x: int, y: int):
        """
        重置位置信息
        :param x: x坐标
        :param y: y坐标
        :return:
        """
        self.pos_x = x
        self.pos_y = y
        self.rect = pygame.Rect(self.pos_x + 65, self.pos_y + 58, 20, 20)

    def draw(self, surface: pygame.Surface, x: int, y: int):
        image = self.walk.get_current_image(self.dir)
        surface.blit(image, (self.pos_x - x, self.pos_y - y))

    def key_move(self, key: int, obstacle_group: pygame.sprite.Group):
        temp_y = self.pos_y
        temp_x = self.pos_x
        # 计算运动后坐标
        if key == K_UP:
            self.dir = 2
            temp_x -= self.step
            temp_y -= self.step
        elif key == K_DOWN:
            self.dir = 0
            temp_x += self.step
            temp_y += self.step
        elif key == K_LEFT:
            self.dir = 1
            temp_x -= self.step
            temp_y += self.step
        elif key == K_RIGHT:
            self.dir = 3
            temp_x += self.step
            temp_y -= self.step
        else:
            return None
        self.rect = pygame.Rect(temp_x + 65, temp_y + 58, 20, 20)
        collide_list = pygame.sprite.spritecollide(self, obstacle_group, False)

        if len(collide_list) > 0:
            self.rect = pygame.Rect(self.pos_x + 65, self.pos_y + 58, 20, 20)
            return None
        else:
            return self.__move__()

    # 0 下 1 左 2 上 3 右
    def __move__(self):
        if self.dir == 2:
            x = -self.step
            y = -self.step
        elif self.dir == 0:
            x = self.step
            y = self.step
        elif self.dir == 1:
            x = -self.step
            y = self.step
        else:
            x = self.step
            y = -self.step
        self.pos_x += x
        self.pos_y += y
        self.rect = pygame.Rect(self.pos_x + 65, self.pos_y + 58, 20, 20)
        return [x, y]