import os
import sys
import pygame
from utils.tiled_render import TiledRenderer
from pygame.constants import QUIT


class Goder:
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image_count = 10
        self.width = 58
        self.height = 83
        # 图片加载
        self.image_array = []
        index = 0
        while index < self.image_count:
            img_path = os.path.join('../resource', 'img', 'god', '0214-16505471-0000' + str(index) + '.tga')
            self.image_array.append(pygame.image.load(img_path))
            index += 1
        self.cur_index = 0
        self.rect = pygame.Rect(pos_x, pos_y, self.width, self.height)

    def draw(self, surface):
        image = self.image_array[self.cur_index]
        surface.blit(image, (self.pos_x, self.pos_y))
        self.cur_index += 1
        if self.cur_index >= self.image_count:
            self.cur_index = 0

    def control(self, x, y):
        self.pos_x += x
        self.pos_y += y
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("我的游戏")
tmx_path = os.path.join('../resource', "tmx", 'map.tmx')
render = TiledRenderer(tmx_path)
surface = pygame.Surface(render.pixel_size)
# 调用render_map渲染得到地图
render.render_map(surface)
goder = Goder(50, 50)
clock = pygame.time.Clock()
step = 20
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                goder.control(-step, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                goder.control(step, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                goder.control(step, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                goder.control(-step, 0)
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()

    goder.draw(surface)
    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock.tick(40)