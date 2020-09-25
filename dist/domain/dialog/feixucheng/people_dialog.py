import os

import pygame

from dialog import blit_text


class PeopleDialog:
    def __init__(self):
        """
        土地公对话框的构建
        """
        # 1.头像照片
        img_path = os.path.join('resource', 'img', 'head', '4.tga')
        temp_header = pygame.image.load(img_path)
        header_w = temp_header.get_width() // 5
        header_h = temp_header.get_height() // 5
        # 头像缩小一半
        header = pygame.transform.scale(temp_header, (header_w, header_h))
        # 2 对话框图片
        dialog_path = os.path.join('resource', 'img', 'ditu', 'beijing1.png')
        temp_dialog = pygame.image.load(dialog_path)
        dialog_w = temp_dialog.get_width() // 1
        dialog_h = temp_dialog.get_height() // 4
        # 会话框缩小一半
        dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        # 3.绘制文字
        font_path = os.path.join('resource', 'font', '迷你简粗宋.TTF')
        font = pygame.font.Font(font_path, 20)
        text = "   目前所有叛乱者的主要头目已经被击杀，边境得到了安宁，从此陛下的江山得到稳固。 \n" \
                "     \n" \
               "                是否前往京城复命。Y/N"
        blit_text(dialog, text, (4, 8), font)

        # 4.生成surface并绘制
        if header_h > dialog_h:
            # h = header_h
            h = dialog_h
        else:
            h = dialog_h
        # w = header_w + dialog_w
        w = dialog_w
        self.surface = pygame.Surface((w, h))
        # 5. 设置关键色，形成透明图片
        self.surface.set_colorkey((0, 0, 0))
        # 6.把头像和对话框绘制上去
        # self.surface.blit(header, (0, 0))
        self.surface.blit(dialog, (0, 0))