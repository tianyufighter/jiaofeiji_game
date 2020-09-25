import os
import sys
import pygame
from pygame.constants import QUIT

from utils.tiled_render import TiledRenderer

# pygame 初始化
pygame.init()
# 初始化窗口
screen = pygame.display.set_mode((800, 600), 0, 32)
# 设置标题栏
pygame.display.set_caption('TMX 地图的显示')
# tmx的路径
tmx_path = os.path.join('../resource', 'tmx', 'huanggong.tmx')
# tmx的渲染类TiledRenderer
render = TiledRenderer(tmx_path)
# 建立新的surface，大小和tmx瓦格设置的尺寸一致
surface = pygame.Surface(render.pixel_size)
# 调用render_map渲染得到地图
render.render_map(surface)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(surface, (0, 0))
    pygame.display.update()
