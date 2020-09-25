import os

import pygame

from dialog import blit_text


class PeopleDialog1:
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
        dialog_path = os.path.join('resource', 'img', 'ditu', 'beijing3.tga')
        temp_dialog = pygame.image.load(dialog_path)
        dialog_w = temp_dialog.get_width() // 1
        dialog_h = temp_dialog.get_height() // 2
        # 会话框缩小一半
        dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        # 3.绘制文字
        font_path = os.path.join('resource', 'font', '迷你简粗宋.TTF')
        font = pygame.font.Font(font_path, 20)
        text = "   \n" \
               "    \n" \
               "            如今天真国周边多次遭到胡人入侵，且叛乱者也为非作歹， \n" \
               "            边境骚乱年年不断，皇帝与众位大臣商议了此事，决定让天真 \n" \
               "            国的大将军平定战乱，皇帝于是派遣人去招樊将军进宫议事。  \n" \
               "            共同商议怎样处理此次叛乱......"
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