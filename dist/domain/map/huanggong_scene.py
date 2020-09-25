"""
皇宫场景
"""
import os
import pygame
from pytmx import pytmx

from dialog.huanggong.people_dialog import PeopleDialog1
from dialog.huanggong.people_dialog2 import PeopleDialog2
from map import TiledScene, FadeScene, SceneStatus, SceneResult
from pygame.constants import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_y, K_SPACE

from role.huanggong.guan1 import Guan1
from role.huanggong.guan2 import Guan2
from role.huanggong.guan3 import Guan3
from role.huanggong.guan4 import Guan4
from role.huanggong.guan5 import Guan5
from role.huanggong.guan6 import Guan6
from role.huanggong.huang import Huang
from role.huanggong.zhan12 import Zhan12
from role.huanggong.zhan34 import Zhan34


class HuangGongScene:
    """
    皇宫场景
    """
    def __init__(self, surface: pygame.Surface, jiang):
        """
        村庄场景初始化
        :param surface: 窗口绘制surface
        """
        self.scene_result = SceneResult.Ongoing
        self.screen = surface
        tiled_path = os.path.join('resource', 'tmx', 'huanggong.tmx')
        # 建立瓦格对象
        self.tiled = TiledScene(tiled_path)
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)
        self.jiang = jiang
        self.huang = None
        self.map_x = 0
        self.map_y = 0
        self.people_group = []
        self.obstacle_group = pygame.sprite.Group()
        self.init_actor()
        # 临时surface
        self.temp_surface = self.tiled.surface.copy()
        self.xian1 = True
        self.xian2 = True
        self.dialog1 = PeopleDialog1()
        self.dialog2 = PeopleDialog2()
        sound_path = os.path.join("resource", "sound", "bei.mp3")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # 循环播放

    def init_actor(self):
        """
        初始化角色
        :return:
        """
        for group in self.tiled.tiled.tmx_data.objectgroups:
            if isinstance(group, pytmx.TiledObjectGroup):
                if group.name == 'guan':
                    for obj in group:
                        if obj.name == 'guan1':
                            guan1 = Guan1(obj.x - 50, obj.y - 50)
                            self.people_group.append(guan1)
                        if obj.name == 'guan2':
                            guan2 = Guan2(obj.x - 50, obj.y - 50)
                            self.people_group.append(guan2)
                        if obj.name == 'guan3':
                            guan3 = Guan3(obj.x - 50, obj.y - 50)
                            self.people_group.append(guan3)
                        if obj.name == 'guan4':
                            guan4 = Guan4(obj.x - 50, obj.y - 50)
                            self.people_group.append(guan4)
                        if obj.name == 'guan5':
                            guan5 = Guan5(obj.x - 50, obj.y - 50)
                            self.people_group.append(guan5)
                        if obj.name == 'guan6':
                            guan6 = Guan6(obj.x - 50, obj.y - 50)
                            self.people_group.append(guan6)
                if group.name == "zhan":
                    for obj in group:
                        if obj.name == 'zhan1':
                            zhan1 = Zhan12(obj.x - 50, obj.y - 50)
                            self.people_group.append(zhan1)
                        if obj.name == 'zhan2':
                            zhan2 = Zhan12(obj.x - 50, obj.y - 50)
                            self.people_group.append(zhan2)
                        if obj.name == 'zhan3':
                            zhan3 = Zhan34(obj.x - 50, obj.y - 50)
                            self.people_group.append(zhan3)
                        if obj.name == 'zhan4':
                            zhan4 = Zhan34(obj.x - 50, obj.y - 50)
                            self.people_group.append(zhan4)
                if group.name == 'huang':
                    for obj in group:
                        if obj.name == 'huang':
                            self.huang = Huang(obj.x - 50, obj.y - 50)

                if group.name == 'jiang':
                    for obj in group:
                        if obj.name == 'jiang':
                            self.jiang.reset_pos(obj.x - 50, obj.y - 50)
                            self.map_x = obj.x - 400
                            self.map_y = obj.y - 300
                if group.name == 'obstacle':
                    for obj in group:
                        obstacle = pygame.sprite.Sprite()
                        obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.obstacle_group.add(obstacle)

    def get_current_surface(self) -> pygame.Surface:
        # 得到子图
        sub_surface = self.fade.get_back_image(self.map_x, self.map_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        # 守卫的绘制
        for temp in self.people_group:
            if self.map_x <= temp.pos_x <= self.map_x + 800:
                if self.map_y <= temp.pos_y <= self.map_y + 600:
                    temp.draw(self.temp_surface, self.map_x, self.map_y)
        # 主角的绘制
        self.jiang.draw(self.temp_surface, self.map_x, self.map_y)
        # 皇上的绘制
        self.huang.draw(self.temp_surface, self.map_x, self.map_y)
        if self.xian1 and self.jiang.huang == 0:
            self.temp_surface.blit(self.dialog1.surface, (0, 400))
        if self.xian2 and self.jiang.huang == 1:
            self.temp_surface.blit(self.dialog2.surface, (0, 400))
        return self.temp_surface

    def run(self):
        """
        场景的运行
        """
        scene_exit = False
        clock = pygame.time.Clock()
        self.huang.sum = self.jiang.huang
        while not scene_exit:
            flag = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.scene_result = SceneResult.Quit
                    scene_exit = True

                if event.type == KEYDOWN:
                    flag = True
                    value = event.key
            if flag:
                temp_pos = self.jiang.key_move(value, self.obstacle_group)
                if temp_pos:
                    if 0 < self.map_x + temp_pos[0] <= (5760 - 800) and 0 < self.map_y + temp_pos[1] <= (4320 - 600):
                        self.map_x += temp_pos[0]
                        self.map_y += temp_pos[1]
                # 如果对话中，并且按键Y同意进入第二个场景
                if self.huang.stop and value == K_y:
                    if self.jiang.huang == 1:
                        self.scene_result = SceneResult.Win
                    self.fade.set_status(SceneStatus.Out) # 设置状态为渐出
                    self.huang.stop = False
                if value == K_SPACE:
                    self.xian1 = False
                if value == K_SPACE and self.jiang.huang == 1:
                    self.xian2 = False
            if self.fade.get_out():
                self.jiang.huang += 1
                scene_exit = True  # 渐出效果执行完毕

            # 场景处于渐出状态时，巫师不与主角进行碰撞检查
            if self.fade.status != SceneStatus.Out:
                self.huang.isCollide(self.jiang)
                for temp in self.people_group:
                    temp.isCollide(self.jiang)

            current_screen = self.get_current_surface()
            self.screen.blit(current_screen, (0, 0))
            pygame.display.update()
            clock.tick(8)

        return scene_exit
