import os

import pygame


class Action:
    """
    角色基本活动
    """
    def __init__(self, path: str, prefix: str, image_count: int, is_loop: bool):
        """
        初始角色行为相关行为
        :param path: 路径
        :param prefix: 文件名前缀
        :param image_count: 图片数量
        :param is_loop: 是否循环显示
        """
        self.image_index = 0
        self.action_images = []  # type:[]
        self.image_count = image_count
        self.is_loop = is_loop
        #加载图片的功能
        for i in range(0, image_count):
            st = ''
            if i < 10:
                st = '0' + str(i)
            else:
                st = str(i)
            img_path = os.path.join('resource', 'img', path, prefix + st + '.tga')
            self.action_images.append(pygame.image.load(img_path))

    def get_current_image(self) -> pygame.image:
        """
        获取当前图片
        :return:
        """
        current_img = self.action_images[self.image_index]
        self.image_index += 1
        if self.image_index + 1 >= self.image_count:
            if self.is_loop:
                self.image_index = 0
            else:
                self.image_index = self.image_count - 1

        return current_img

    def is_end(self) -> bool:
        """
        活动是否结束
        :return:
        """
        if self.is_loop:
            return False
        else:
            if self.image_index >= self.image_count - 1:
                return True
            else:
                return False

    def reset(self):
        """
        重置活动
        :return:
        """
        self.image_index = 0


# 0 下 1 左  2 上 3 右
class DirAction:
    """
    带方向的角色活动
    """
    def __init__(self, path: str,
                 prefix: str, dir_count: int, image_count: int, is_loop: bool):
        """
        角色行为
        :param path: 路径
        :param prefix: 文件名前缀
        :param dir_count: 方向数量
        :param image_count: 图片数量
        :param is_loop: 是否循环显示
        """
        self.image_index = 0
        self.action_images = []  # type:[]
        self.image_count = image_count
        self.dir = 0
        self.is_loop = is_loop

        for j in range(0, dir_count):
            dir_image = []
            for i in range(0, image_count):
                img_path = os.path.join('resource', 'img', path, prefix +
                                        str.format("%02d" % j) + str.format("%03d" % i) + '.tga')
                dir_image.append(pygame.image.load(img_path))
            self.action_images.append(dir_image)

    def get_current_image(self, dir: int) -> pygame.image:
        """
        获取当前图片
        :param dir: 获取的方向
        :return:
        """
        current_img = self.action_images[dir][self.image_index]
        self.image_index += 1
        if self.image_index + 1 >= self.image_count:
            if self.is_loop:
                self.image_index = 0
            else:
                self.image_index = self.image_count - 1

        return current_img

    def is_end(self) -> bool:
        """
        活动是否结束
        :return:
        """
        if self.is_loop:
            return False
        else:
            if self.image_index >= self.image_count - 1:
                return True
            else:
                return False

    def reset(self):
        """
        重置活动
        :return:
        """
        self.image_index = 0
