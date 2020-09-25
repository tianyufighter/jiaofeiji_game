import os
import sys
import pygame
from pygame.constants import QUIT

# pygame 初始化
pygame.init()
'''
说明：路径拼接 
参考文档 https://docs.python.org/zh-cn/3/library/os.path.html#module-os.path
'''
back_img_path = os.path.join('../resource', 'image', 'pic.jpg')

'''
说明：加载图片
参考文档 https://www.pygame.org/docs/ref/image.html#pygame.image.load
'''
background = pygame.image.load(back_img_path)

'''
说明：初始化显示窗口
参考文档 https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
'''
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('PyGame 我的背景图片')
# icon_path = os.path.join('./resource', 'imag', 'icon', '1.png')
# icon = pygame.image.load(icon_path)
# pygame.display.set_icon(icon)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    '''
    说明：绘制图片
    参考文档 https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit
    '''
    screen.blit(background, (0, 0))

    '''
    说明：更新显示
    参考文档 https://www.pygame.org/docs/ref/display.html#pygame.display.update
    '''
    pygame.display.update()
