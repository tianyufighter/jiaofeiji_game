"""
村庄的场景
"""
import os
import pygame
from pytmx import pytmx

from pygame.constants import QUIT, KEYDOWN, K_y, K_SPACE

from dialog.feixucheng.background_dialog import RoleDialog
from dialog.feixucheng.battle_dialog1 import BattleDialog1
from dialog.feixucheng.battle_dialog2 import BattleDialog2
from dialog.feixucheng.battle_dialog3 import BattleDialog3
from dialog.feixucheng.battle_dialog4 import BattleDialog4
from dialog.feixucheng.people_dialog import PeopleDialog
from map import SceneResult, TiledScene, FadeScene, SceneStatus
from role.feixucheng.people1 import People1
from role.feixucheng.people2 import People2
from role.feixucheng.people3 import People3
from role.feixucheng.people4 import People4


class FeiXuChengScene:
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
        tiled_path = os.path.join("resource", "tmx", "feixucheng.tmx")
        # 建立瓦格对象
        self.tiled = TiledScene(tiled_path)
        self.biao1 = None
        self.biao2 = None
        self.biao3 = None
        self.biao4 = None
        # 判断用户在打斗结束时是否按了y切换下一个场景
        # self.biao2 = False
        # 渐变对象
        self.fade = FadeScene(self.tiled.surface)

        self.obstacle_group = pygame.sprite.Group()

        # self.people_group = []
        # 人物对象
        self.people1 = None
        self.people2 = None
        self.people3 = None
        self.people4 = None
        # 敌人组
        self.monster_group1 = pygame.sprite.Group()
        self.monster_group2 = pygame.sprite.Group()
        self.monster_group3 = pygame.sprite.Group()
        self.monster_group4 = pygame.sprite.Group()
        self.jiang = jiang
        self.map_x = 0
        self.map_y = 0
        self.init_actor()

        # 临时surface
        self.temp_surface = pygame.Surface((800, 600))

        # 设置战斗的对话框
        self.battle_dialog1 = None
        self.battle_dialog2 = None
        self.battle_dialog3 = None
        self.battle_dialog4 = None

        self.dialog = PeopleDialog()
        self.sum = 0

        self.dialog2 = RoleDialog()
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
                if group.name == 'jiang':
                    for obj in group:
                        if obj.name == 'jiang':
                            self.jiang.reset_pos(obj.x - 50, obj.y - 50)
                            self.map_x = obj.x - 400
                            self.map_y = obj.y - 300

                if group.name == 'people':
                    for obj in group:
                        if obj.name == 'people1':
                            self.people1 = People1(obj.x - 50, obj.y - 50)
                        if obj.name == 'fp1':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster_group1.add(monster)
                        if obj.name == 'people2':
                            self.people2 = People2(obj.x - 55, obj.y - 70)
                        if obj.name == 'fp2':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster_group2.add(monster)
                        if obj.name == 'people3':
                            self.people3 = People3(obj.x - 50, obj.y - 50)
                        if obj.name == 'fp3':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster_group3.add(monster)
                        if obj.name == 'people4':
                            self.people4 = People4(obj.x - 50, obj.y - 50)
                        if obj.name == 'fp4':
                            monster = pygame.sprite.Sprite()
                            monster.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.monster_group4.add(monster)

    def get_current_surface(self) -> pygame.Surface:
        """
        获取当前显示场景的surface
        :return: 当前显示场景的surface
        """
        # 获取子图
        sub_surface = self.fade.get_back_image(self.map_x, self.map_y)
        self.temp_surface.blit(sub_surface, (0, 0))
        # 将军绘制
        self.jiang.draw(self.temp_surface, self.map_x, self.map_y)
        # 绘制敌人
        if not self.biao1:
            self.people1.draw(self.temp_surface, self.map_x, self.map_y)
        if not self.biao2:
            self.people2.draw(self.temp_surface, self.map_x, self.map_y)
        if not self.biao3:
            self.people3.draw(self.temp_surface, self.map_x, self.map_y)
        if not self.biao4:
            self.people4.draw(self.temp_surface, self.map_x, self.map_y)
        if self.sum == 4:
            self.temp_surface.blit(self.dialog.surface, (0, 500))
        # 绘制打斗
        if self.battle_dialog1 and not self.battle_dialog1.over_show:
            self.battle_dialog1.draw(self.temp_surface)
        if self.battle_dialog2 and not self.battle_dialog2.over_show:
            self.battle_dialog2.draw(self.temp_surface)
        if self.battle_dialog3 and not self.battle_dialog3.over_show:
            self.battle_dialog3.draw(self.temp_surface)
        if self.battle_dialog4 and not self.battle_dialog4.over_show:
            self.battle_dialog4.draw(self.temp_surface)
        # for temp in self.people_group:
        #     if self.map_x <= temp.pos_x <= self.map_x + 800:
        #         if self.map_y <= temp.pos_y <= self.map_y + 600:
        #             # if temp.xu == 1 and not self.biao1:
        #             temp.draw(self.temp_surface, self.map_x, self.map_y)
        #             # if temp.xu == 2 and not self.biao2:
        #             #     temp.draw(self.temp_surface, self.map_x, self.map_y)
        #             # if temp.xu == 3 and not self.biao3:
        #             #     temp.draw(self.temp_surface, self.map_x, self.map_y)
        #             # if temp.xu == 4 and not self.biao4:
        #             #     temp.draw(self.temp_surface, self.map_x, self.map_y)
        if self.xian:
            self.temp_surface.blit(self.dialog2.surface, (0, 400))
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
                    if 0 < self.map_x + temp_pos[0] <= (3200 - 800) and 0 < self.map_y + temp_pos[1] <= (1936 - 600):
                        self.map_x += temp_pos[0]
                        self.map_y += temp_pos[1]
                if self.sum == 4 and pressed_key == K_y:
                    self.fade.set_status(SceneStatus.Out)
                if pressed_key == K_SPACE:
                    self.xian = False
            # 调用打斗场景
            self.create_battle_dialog1()
            self.create_battle_dialog2()
            self.create_battle_dialog3()
            self.create_battle_dialog4()
            # 打斗处理
            if self.battle_dialog1 and not self.battle_dialog1.over_show:
                self.battle_dialog1.process(key_down, pressed_key)
                self.jiang.hp = self.battle_dialog1.jiang.hp

            if self.battle_dialog2 and not self.battle_dialog2.over_show:
                self.battle_dialog2.process(key_down, pressed_key)
                self.jiang.hp = self.battle_dialog2.jiang.hp

            if self.battle_dialog3 and not self.battle_dialog3.over_show:
                self.battle_dialog3.process(key_down, pressed_key)
                self.jiang.hp = self.battle_dialog3.jiang.hp

            if self.battle_dialog4 and not self.battle_dialog4.over_show:
                self.battle_dialog4.process(key_down, pressed_key)
                self.jiang.hp = self.battle_dialog4.jiang.hp

            # 当打斗框消失后，这个敌人不画在地图上
            # if self.battle_dialog1 and s:
            #     self.biao1 = True
            # if not self.battle_dialog2:
            #     self.biao2 = True
            # if not self.battle_dialog3:
            #     self.biao3 = True
            # if not self.battle_dialog4:
            #     self.biao4 = True
            self.sum = 0
            # 设置四个标记，判断每个场景是否已经出现过
            f1 = 0
            f2 = 0
            f3 = 0
            f4 = 0
            if self.battle_dialog1 and self.battle_dialog1.over_show:
                f1 = 1
                self.biao1 = True
                if self.jiang.hp < 0:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
                elif self.jiang.hp > 110:
                    self.scene_result = SceneResult.Win
                    scene_exit = True
            if self.battle_dialog2 and self.battle_dialog2.over_show:
                f2 = 1
                self.biao2 = True
                if self.jiang.hp < 0:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
                elif self.jiang.hp > 110:
                    self.scene_result = SceneResult.Win
                    scene_exit = True
            if self.battle_dialog3 and self.battle_dialog3.over_show:
                f3 = 1
                self.biao3 = True
                if self.jiang.hp < 0:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
                elif self.jiang.hp > 110:
                    self.scene_result = SceneResult.Win
                    scene_exit = True
            if self.battle_dialog4 and self.battle_dialog4.over_show:
                f4 = 1
                self.biao4 = True
                if self.jiang.hp < 0:
                    self.scene_result = SceneResult.Fail
                    scene_exit = True
                elif self.jiang.hp > 110:
                    self.scene_result = SceneResult.Win
                    scene_exit = True
                # elif self.battle_dialog.biao3:
                #     # 判断是否在打斗场景中进入下一个地图
                #     if self.fade.status != SceneStatus.Out:
                #         self.fade.set_status(SceneStatus.Out)

            if f1:
                self.sum += 1
            if f2:
                self.sum += 1
            if f3:
                self.sum += 1
            if f4:
                self.sum += 1
            if self.fade.get_out():
                scene_exit = True
            # 场景处于渐出状态时，人物不与主角进行碰撞检查
            # if self.fade.status != SceneStatus.Out:
            #     self.people1.isCollide(self.jiang)
            #     self.people2.isCollide(self.jiang)
            #     self.people3.isCollide(self.jiang)
            #     self.people4.isCollide(self.jiang)
                # for temp in self.people_group:
                #     temp.isCollide(self.jiang)
            current_screen = self.get_current_surface()
            self.screen.blit(current_screen, (0, 0))
            pygame.display.update()
            clock.tick(10)
        return scene_exit

    def create_battle_dialog1(self):
        """
        创建打斗场景
        """
        flag = False
        if self.battle_dialog1 is None:
            flag = True
        elif self.battle_dialog1.over_show:
            flag = True

        if flag:
            collide_list = pygame.sprite.spritecollide(self.jiang, self.monster_group1, True)
            if collide_list:
                self.battle_dialog1 = BattleDialog1(self.jiang.hp)

    def create_battle_dialog2(self):
        """
        创建打斗场景
        """
        flag = False
        if self.battle_dialog2 is None:
            flag = True
        elif self.battle_dialog2.over_show:
            flag = True

        if flag:
            collide_list = pygame.sprite.spritecollide(self.jiang, self.monster_group2, True)
            if collide_list:
                self.battle_dialog2 = BattleDialog2(self.jiang.hp)

    def create_battle_dialog3(self):
        """
        创建打斗场景
        """
        flag = False
        if self.battle_dialog3 is None:
            flag = True
        elif self.battle_dialog3.over_show:
            flag = True

        if flag:
            collide_list = pygame.sprite.spritecollide(self.jiang, self.monster_group3, True)
            if collide_list:
                self.battle_dialog3 = BattleDialog3(self.jiang.hp)

    def create_battle_dialog4(self):
        """
        创建打斗场景
        """
        flag = False
        if self.battle_dialog4 is None:
            flag = True
        elif self.battle_dialog4.over_show:
            flag = True

        if flag:
            collide_list = pygame.sprite.spritecollide(self.jiang, self.monster_group4, True)
            if collide_list:
                self.battle_dialog4 = BattleDialog4(self.jiang.hp)