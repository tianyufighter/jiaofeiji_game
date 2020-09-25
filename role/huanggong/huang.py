import random
import pygame

from dialog.huanggong.huang_dialog import HuangDialog
from dialog.huanggong.huang_dialog2 import HuangDialog2
from role import DirAction


class Huang(pygame.sprite.Sprite):
    """
    皇上
    """
    def __init__(self, x, y):
        self.walk = DirAction("wang1", "0845-558b14d5-", 4, 8, True)
        self.pos_x = x
        self.pos_y = y
        self.width = 106
        self.height = 109
        self.dir = 0
        self.step = 2
        self.step_count = 0
        self.stop = False
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width + 20, self.height + 20)
        self.dialog1 = HuangDialog()
        self.dialog2 = HuangDialog2()
        self.sum = 0

    def draw(self, surface, x, y):
        """
        绘制函数
        :param surface: 背景
        :param x: 窗口x坐标
        :param y: 窗口y坐标
        :return:
        """
        image = self.walk.get_current_image(self.dir)
        if self.stop:
            if self.sum == 0:
                surface.blit(self.dialog1.surface, (self.pos_x - x, self.pos_y - y + self.height))
            if self.sum == 1:
                surface.blit(self.dialog2.surface, (self.pos_x - x, self.pos_y - y + self.height))
        surface.blit(image, (self.pos_x - x, self.pos_y - y))
        self.__move__()

    def __move__(self):
        if self.stop:
            return
        self.step_count += 1
        if self.dir == 0:
            self.pos_x += self.step
            if self.pos_x < 0 or self.pos_x > (5760 - self.width):
                self.pos_x -= self.step
            self.pos_y += self.step
            if self.pos_y > 0 or self.pos_y > (4320 - self.height):
                self.pos_y -= self.step
        elif self.dir == 1:
            self.pos_x -= self.step
            if self.pos_x < 0 or self.pos_x > (5760 - self.width):
                self.pos_x += self.step
            self.pos_y += self.step
            if self.pos_y > 0 or self.pos_y > (4320 - self.height):
                self.pos_y -= self.step
        elif self.dir == 2:
            self.pos_x -= self.step
            if self.pos_x < 0 or self.pos_x > (5760 - self.width):
                self.pos_x += self.step
            self.pos_y -= self.step
            if self.pos_y > 0 or self.pos_y > (4320 - self.height):
                self.pos_y += self.step
        elif self.dir == 3:
            self.pos_x += self.step
            if self.pos_x < 0 or self.pos_x > (5760 - self.width):
                self.pos_x -= self.step
            self.pos_y -= self.step
            if self.pos_y > 0 or self.pos_y > (4320 - self.width):
                self.pos_y += self.step

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

        if self.step_count == 20:
            self.step_count = 0
            num = random.randrange(0, 4, 1)
            self.dir = num

    def isCollide(self, role):
        if pygame.sprite.collide_rect(self, role):
            self.stop = True
        else:
            self.stop = False

