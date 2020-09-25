import os
import sys
import pygame
from utils.tiled_render import TiledRenderer
from pygame.constants import QUIT

class Older(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int):
        """
        老人类的构造函数 （位置 图片 RECT）
        :param pos_x: 初始x位置
        :param pos_y: 初始y位置
        """
        # 保存位置信息
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image_count = 10
        self.width = 58
        self.height = 83

        # 图片加载
        self.older_image = []
        i = 0
        while i < self.image_count:
            img_path = os.path.join('../resource', 'img', 'elder', 'elder1-0000' + str(i) + '.tga')
            self.older_image.append(pygame.image.load(img_path))
            i = i + 1
        # 当前图片的位置
        self.image_index = 0
        # 当前区域位置
        self.rect = pygame.Rect(pos_x, pos_y, self.width, self.height)

    def draw(self, surface):
        """
        绘制函数
        :param surface: 背景绘制区域
        :return:
        """
        image = self.older_image[self.image_index]
        surface.blit(image, (self.pos_x, self.pos_y))
        self.image_index += 1
        if self.image_index >= self.image_count:
            self.image_index = 0


# pygame 初始化
pygame.init()
# 初始化窗口
screen = pygame.display.set_mode((800, 600), 0, 32)
# 设置标题栏
pygame.display.set_caption('TMX 地图的显示')
# tmx的路径
tmx_path = os.path.join('../resource', 'map1.tmx')
# tmx的渲染类TiledRenderer
render = TiledRenderer(tmx_path)
# 建立新的surface，大小和tmx瓦格设置的尺寸一致
surface = pygame.Surface(render.pixel_size)
# 调用render_map渲染得到地图
render.render_map(surface)

older = Older(100, 100)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    older.draw(surface)
    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock.tick(40)
