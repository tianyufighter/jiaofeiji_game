import enum
import os

import pygame
from pygame.constants import K_ESCAPE, K_y, K_n

from dialog import blit_text
from map import SceneResult
from role.feixucheng.jiang_battle import BattleJiang, JiangBattleStatus
from role.feixucheng.p2_battle import BattleP2, DiBattleStatus


class BattleStatus(enum.IntEnum):
    """
    战斗场景状态
    """
    Swk_dialog = 0
    Swk_fight = 1
    Enemy_fight = 2
    Fail = 3
    Win = 4
    Escape = 5


class BattleDialog2:
    # 初始化当前状态
    status = BattleStatus.Swk_dialog

    def __init__(self, swk_hp: int):
        """
        设置战斗场景中的各个属性值
        :param swk_hp: 孙悟空生命值
        """
        self.flag1 = 2
        self.flag2 = False
        self.scene_result = SceneResult.Ongoing
        self.jiang = BattleJiang(swk_hp)
        self.monster = BattleP2()
        # 当打斗完成后，还没有按esc时，显示切换地图的文本
        # self.biao2 = False
        # 切换游戏地图，从博莱城到下一张地图的标记
        # self.biao3 = False
        # 背景相关初始化
        dialog_file = os.path.join('resource', 'img', 'ditu', '7.jpg')
        temp_dialog = pygame.image.load(dialog_file)
        dialog_w = temp_dialog.get_width()
        dialog_h = temp_dialog.get_height()
        # 会话框缩小一半
        self.dialog = pygame.transform.scale(temp_dialog, (dialog_w // 1, dialog_h // 1))
        # 设置图片透明度
        self.dialog.set_alpha(255)

        self.dialog_width = self.dialog.get_width()
        self.dialog_height = self.dialog.get_height()
        # 对话相关文本和字体
        font_path = os.path.join('resource', 'font', '迷你简粗宋.TTF')
        self.font = pygame.font.Font(font_path, 18)
        self.text = "看 我 一 剑。y " \
                    "下 次 来 战。n "

        # self.text1 = "叛 乱 者 逃 亡  \n" \
        #              " 到 了 五 庄 观。  \n" \
        #              " 前 往 寺 庙。y  \n" \
        #              " 下 此 来 战。n  \n"

        # 设置显示状态
        self.over_show = False
        sound_path1 = os.path.join("resource", "sound", "da1.wav")
        sound_path2 = os.path.join("resource", "sound", "da2.wav")
        self.swk_music = pygame.mixer.Sound(sound_path1)
        self.monster_music = pygame.mixer.Sound(sound_path2)
        # sound_path3 = os.path.join("resource", "sound", "shou1.wav")
        # sound_path4 = os.path.join("resource", "sound", "shou2.wav")
        # self.swk_music2 = pygame.mixer.Sound(sound_path3)
        # self.monster_music2 = pygame.mixer.Sound(sound_path4)
        pygame.mixer.music.set_volume(5)  # 设置音量

    def process(self, key_down: bool, pressed_key: int):
        # 孙悟空死亡结束
        if self.jiang.status == JiangBattleStatus.DieOver:
            self.status = BattleStatus.Fail
            self.scene_result = SceneResult.Fail
            self.swk_music.stop()
            self.monster_music.stop()
            # self.biao2 = True
            if key_down and pressed_key == K_ESCAPE:
                self.flag2 = True
                self.over_show = True
            # if key_down and pressed_key == K_y:
            #     self.over_show = True
            #     self.biao3 = True
            # if key_down and pressed_key == K_n:
            #     self.over_show = True
            return

        # 孙悟空逃跑结束
        if self.jiang.status == JiangBattleStatus.EscapeOver:
            self.status = BattleStatus.Escape
            self.scene_result = SceneResult.Fail
            self.swk_music.stop()
            self.monster_music.stop()
            # self.biao2 = True
            if key_down and pressed_key == K_ESCAPE:
                self.flag2 = True
                self.over_show = True
            # self.over_show = True
            # if key_down and pressed_key == K_y:
            #     self.over_show = True
            #     self.biao3 = True
            # if key_down and pressed_key == K_n:
            #     self.over_show = True
            return
        # 牛魔王死亡结束
        if self.monster.status == JiangBattleStatus.DieOver:
            self.status = BattleStatus.Win
            self.scene_result = SceneResult.Win
            self.swk_music.stop()
            self.monster_music.stop()
            # self.biao2 = True
            if key_down and pressed_key == K_ESCAPE:
                self.flag2 = True
                self.over_show = True
            # self.over_show = True
            # if key_down and pressed_key == K_y:
            #     self.over_show = True
            #     self.biao3 = True
            # if key_down and pressed_key == K_n:
            #     self.over_show = True
            return

        # 牛魔王逃跑结束
        if self.monster.status == DiBattleStatus.EscapeOver:
            self.status = BattleStatus.Escape
            self.scene_result = SceneResult.Win
            self.swk_music.stop()
            self.monster_music.stop()
            # self.biao2 = True
            if key_down and pressed_key == K_ESCAPE:
                self.flag2 = True
                self.over_show = True
            # self.over_show = True
            # self.over_show = True
            # if key_down and pressed_key == K_y:
            #     self.over_show = True
            #     self.biao3 = True
            # if key_down and pressed_key == K_n:
            #     self.over_show = True
            return

        # 孙悟空死亡逃跑过程
        if self.jiang.status == JiangBattleStatus.Die or self.jiang.status == JiangBattleStatus.Escape:
            self.jiang.action_over()
            return

        # 牛魔王死亡过程
        if self.monster.status == DiBattleStatus.Die:
            self.monster.action_over()
            return
        # 牛魔王逃跑过程
        if self.monster.status == DiBattleStatus.Escape:
            self.monster.action_over()
            return
        # 对话框状态
        if self.status == BattleStatus.Swk_dialog:
            # 孙悟空打斗
            if key_down and pressed_key == K_y:
                self.swk_music.stop()
                self.monster_music.stop()
                self.status = BattleStatus.Swk_fight
                self.jiang.set_status(JiangBattleStatus.Fight)
                self.monster.set_status(DiBattleStatus.Station)
                self.swk_music.play()
                # self.monster_music2.play()
            # 孙悟空逃跑
            if key_down and pressed_key == K_n:
                self.swk_music.stop()
                self.monster_music.stop()
                self.status = BattleStatus.Escape
                self.monster.set_status(DiBattleStatus.Station)
                self.jiang.set_status(JiangBattleStatus.Escape)
                self.swk_music.stop()
                self.monster_music.stop()

        # 孙悟空打斗
        if self.status == BattleStatus.Swk_fight:
            if self.jiang.action_over():
                # 切换状态
                self.swk_music.stop()
                self.monster_music.stop()
                self.status = BattleStatus.Enemy_fight
                self.jiang.set_status(JiangBattleStatus.Station)
                self.monster.set_status(DiBattleStatus.Fight)
                # 后减生命值
                self.monster.attack_hp(-10)
                self.jiang.attack_hp(10)
                if self.monster.hp < 0:
                    return
                self.monster_music.play()
                # self.monster_music2.play()
                return

        if self.status == BattleStatus.Enemy_fight:
            if self.monster.action_over():
                self.swk_music.stop()
                self.monster_music.stop()
                self.status = BattleStatus.Swk_dialog
                self.jiang.set_status(JiangBattleStatus.Station)
                self.monster.set_status(DiBattleStatus.Station)
                self.jiang.attack_hp(-30)
                return

    def draw(self, surface):
        """
        绘制
        :param surface: 背景
        :return:
        """
        # if not self.biao3:
        # 干净的背景
        dialog = self.dialog.copy()
        # 文本的显示是状态来的
        if self.status == BattleStatus.Swk_dialog:
            blit_text(dialog, self.text, (600, 500), self.font)
        # if self.biao2:
        #     blit_text(dialog, self.text1, (600, 500), self.font)
        self.jiang.draw(dialog)
        self.monster.draw(dialog)

        surface.blit(dialog, (800 / 2 - self.dialog_width / 2, 600 / 2 - self.dialog_height / 2))
