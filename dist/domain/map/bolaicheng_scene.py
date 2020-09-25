"""
村庄的场景
"""
import os
import pygame
from pytmx import pytmx

from pygame.constants import QUIT, KEYDOWN, K_SPACE

from dialog.bolaicheng.background_dialog import RoleDialog
from dialog.bolaicheng.battle_dialog import BattleDialog
from map import SceneResult, TiledScene, FadeScene, SceneStatus
from role.bolaicheng.di import Di
from role.bolaicheng.people1 import People1
from role.bolaicheng.people10 import People10
from role.bolaicheng.people11 import People11
from role.bolaicheng.people12 import People12
from role.bolaicheng.people13 import People13
from role.bolaicheng.people14 import People14
from role.bolaicheng.people2 import People2
from role.bolaicheng.people3 import People3
from role.bolaicheng.people4 import People4
from role.bolaicheng.people5 import People5
from role.bolaicheng.people6 import People6
from role.bolaicheng.people7 import People7
from role.bolaicheng.people8 import People8
from role.bolaicheng.people9 import People9


class BoLaiChengScene:
    """
    寺庙场景
    """
    scene_result = SceneResult.Ongoing

    def __init__(self, surface: pygame.Surface, jiang):
        """
        寺庙场景初始化
        :param surface: 窗口绘制的surface
        """
        self.screen = surface
        tiled_path = os.path.join("resource", "tmx", "bolai.tmx")
        # 建立瓦格对象
        self.tiled = TiledScene(tiled_path)
        self.di = None
        self.biao = None
        # 判断用户在打斗结束时是否按了y切换下一个场景
        # self.biao2 = False
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)

        self.obstacle_group = pygame.sprite.Group()

        self.people_group = []

        # 敌人组
        self.monster_group = pygame.sprite.Group()
        self.jiang = jiang
        self.map_x = 0
        self.map_y = 0
        self.init_actor()

        # 临时surface
        self.temp_surface = pygame.Surface((800, 600))

        # 设置战斗的对话框
        self.battle_dialog = None
        self.dialog = RoleDialog()
        self.xian = True
        sound_path = os.path.join("resource", "sound", "bei.mp3")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # 循环播放

    def init_actor(self):
        """
        初始化角色人物
        return:
        """
        for group in self.tiled.tiled.tmx_data.objectgroups:
            if isinstance(group, pytmx.TiledObjectGroup):
                if group.name == 'obstacle':
                    for obj in group:
                        obstacle = pygame.sprite.Sprite()
                        obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.obstacle_group.add(obstacle)

                # 敌人组
                if group.name == 'di':
                    for obj in group:
                        if obj.name == 'fdi':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster_group.add(monster)
                        if obj.name == 'di':
                            self.di = Di(obj.x - 55, obj.y - 70)
                if group.name == 'jiang':
                    for obj in group:
                        if obj.name == 'jiang':
                            self.jiang.reset_pos(obj.x - 50, obj.y - 50)
                            self.map_x = obj.x - 400
                            self.map_y = obj.y - 300

                if group.name == 'people':
                    for obj in group:
                        if obj.name == 'people1':
                            people1 = People1(obj.x - 50, obj.y - 50)
                            self.people_group.append(people1)
                        if obj.name == 'people2':
                            people2 = People2(obj.x - 50, obj.y - 50)
                            self.people_group.append(people2)
                        if obj.name == 'people3':
                            people3 = People3(obj.x - 50, obj.y - 50)
                            self.people_group.append(people3)
                        if obj.name == 'people4':
                            people4 = People4(obj.x - 50, obj.y - 50)
                            self.people_group.append(people4)
                        if obj.name == 'people5':
                            people5 = People5(obj.x - 50, obj.y - 50)
                            self.people_group.append(people5)
                        if obj.name == 'people6':
                            people6 = People6(obj.x - 50, obj.y - 50)
                            self.people_group.append(people6)
                        if obj.name == 'people7':
                            people7 = People7(obj.x - 50, obj.y - 50)
                            self.people_group.append(people7)
                        if obj.name == 'people8':
                            people8 = People8(obj.x - 50, obj.y - 50)
                            self.people_group.append(people8)
                        if obj.name == 'people9':
                            people9 = People9(obj.x - 50, obj.y - 50)
                            self.people_group.append(people9)
                        if obj.name == 'people10':
                            people10 = People10(obj.x - 50, obj.y - 50)
                            self.people_group.append(people10)
                        if obj.name == 'people11':
                            people11 = People11(obj.x - 50, obj.y - 50)
                            self.people_group.append(people11)
                        if obj.name == 'people12':
                            people12 = People12(obj.x - 50, obj.y - 50)
                            self.people_group.append(people12)
                        if obj.name == 'people13':
                            people13 = People13(obj.x - 50, obj.y - 50)
                            self.people_group.append(people13)
                        if obj.name == 'people14':
                            people14 = People14(obj.x - 50, obj.y - 50)
                            self.people_group.append(people14)
                        if obj.name == 'people15':
                            people15 = People14(obj.x - 50, obj.y - 50)
                            self.people_group.append(people15)

    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        # 获取子图
        sub_surface = self.fade.get_back_image(self.map_x, self.map_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        # 孙悟空绘制
        self.jiang.draw(self.temp_surface, self.map_x, self.map_y)
        # 绘制敌人
        if self.biao:
            self.di.draw(self.temp_surface, self.map_x, self.map_y)
        # 绘制打斗
        if self.battle_dialog and not self.battle_dialog.over_show:
            self.battle_dialog.draw(self.temp_surface)
        for temp in self.people_group:
            if self.map_x <= temp.pos_x <= self.map_x + 800:
                if self.map_y <= temp.pos_y <= self.map_y + 600:
                    temp.draw(self.temp_surface, self.map_x, self.map_y)
        if self.xian:
            self.temp_surface.blit(self.dialog.surface, (0, 400))
        return self.temp_surface

    def run(self):
        """
        寺庙场景的运行
        :return:
        """
        scene_exit = False
        clock = pygame.time.Clock()
        while not scene_exit:
            self.biao = False
            key_down = False
            pressed_key = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.scene_result = SceneResult.Quit
                    scene_exit = True

                if event.type == KEYDOWN:
                    key_down = True
                    pressed_key = event.key

            if key_down:
                temp_pos = self.jiang.key_move(pressed_key, self.obstacle_group)
                if temp_pos:
                    if 0 < self.map_x + temp_pos[0] <= (7680 - 800) and 0 < self.map_y + temp_pos[1] <= (5760 - 600):
                        self.map_x += temp_pos[0]
                        self.map_y += temp_pos[1]
                if pressed_key == K_SPACE:
                    self.xian = False
            # 调用打斗场景
            self.create_battle_dialog()
            # 打斗处理
            if self.battle_dialog and not self.battle_dialog.over_show:
                self.battle_dialog.process(key_down, pressed_key)
                self.jiang.hp = self.battle_dialog.jiang.hp

            # 当打斗框消失后，这个敌人不画在地图上
            if not self.battle_dialog:
                self.biao = True

            # # 判断是否在打斗场景中进入下一个地图
            # if self.battle_dialog and self.battle_dialog.over_show:
            #     if self.battle_dialog.biao3:
            #         self.fade.set_status(SceneStatus.Out)
            # if self.fade.get_out():
            #     scene_exit = True

            # if self.biao2:
            #     self.fade.set_status(SceneStatus.Out)
            # if self.fade.get_out():
            #     scene_exit = True

            if self.battle_dialog and self.battle_dialog.over_show:
                if self.jiang.hp < 0:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
                elif self.jiang.hp > 110:
                    self.scene_result = SceneResult.Win
                    scene_exit = True
                elif self.battle_dialog.biao3:
                    # 判断是否在打斗场景中进入下一个地图
                    if self.fade.status != SceneStatus.Out:
                        self.fade.set_status(SceneStatus.Out)
            if self.fade.get_out():
                scene_exit = True

            # 场景处于渐出状态时，人物不与主角进行碰撞检查
            if self.fade.status != SceneStatus.Out:
                for temp in self.people_group:
                    temp.isCollide(self.jiang)
            current_screen = self.get_current_surface()
            self.screen.blit(current_screen, (0, 0))
            pygame.display.update()
            clock.tick(10)
        return scene_exit

    def create_battle_dialog(self):
        """
        创建打斗场景
        """
        flag = False
        if self.battle_dialog is None:
            flag = True
        elif self.battle_dialog.over_show:
            flag = True

        if flag:
            collide_list = pygame.sprite.spritecollide(self.jiang, self.monster_group, True)
            if collide_list:
                self.battle_dialog = BattleDialog(self.jiang.hp)
