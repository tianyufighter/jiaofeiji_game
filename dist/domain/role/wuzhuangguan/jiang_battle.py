import enum
import pygame
import role


class JiangBattleStatus(enum.IntEnum):
    """
    将军的状态
    """
    Station = 0
    Fight = 1
    Escape = 2
    EscapeOver = 3
    Die = 4
    DieOver = 5


class BattleJiang(pygame.sprite.Sprite):
    """
    战斗中的将军
    :param hp: 生命值
    """
    def __init__(self, hp: int):
        """
        初始化战斗的孙悟空
        :param hp: 生命值
        """
        pygame.sprite.Sprite.__init__(self) # 调用父类(Sprite)构造函数
        # 魔法战斗
        self.magic_fight = role.Action("magic\\gong", "0390-d20e78bf-000", 17, False)
        # 死亡和逃跑
        self.magic_die_escape = role.Action("magic\\disappear", "0065-22a50569-000", 21, False)
        # 站立行为
        self.station = role.DirAction("wo", "0789-4ee87ee9-", 4, 4, False)

        self.status = JiangBattleStatus.Station
        self.hp = hp
        self.pos_x = 270
        self.pos_y = 450

    def attack_hp(self, hp):
        """
        生命值的改变
        :param hp: 增加或减少的生命值（可正 可负）
        """
        self.hp += hp
        if self.hp <= 0:
            self.set_status(JiangBattleStatus.Die)

    def set_status(self, status):
        """
        修改孙悟空的战斗状态
        :param status: 状态值
        """
        self.status = status
        if status == JiangBattleStatus.Fight:
            self.magic_fight.reset()
        elif status == JiangBattleStatus.Station:
            self.station.reset()
        elif status == JiangBattleStatus.Escape:
            self.magic_die_escape.reset()
        elif status == JiangBattleStatus.Die:
            self.magic_die_escape.reset()

    def action_over(self) -> bool:
        """
        判断一个行为是否结束
        :return: 是否结束
        """
        if self.status == JiangBattleStatus.Station:
            return self.station.is_end()
        elif self.status == JiangBattleStatus.Fight:
            return self.magic_fight.is_end()
        elif self.status == JiangBattleStatus.Escape:
            if self.magic_die_escape.is_end():
                self.status = JiangBattleStatus.EscapeOver
            return self.magic_die_escape.is_end()
        elif self.status == JiangBattleStatus.Die:
            if self.magic_die_escape.is_end():
                self.status = JiangBattleStatus.DieOver
            return self.magic_die_escape.is_end()

    def draw(self, surface: pygame.Surface):
        """
        绘制函数
        :param surface: 背景
        """
        dir = 0
        if self.status == JiangBattleStatus.Station:
            image = self.station.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))
        elif self.status == JiangBattleStatus.Fight:
            image = self.station.get_current_image(dir)
            surface.blit(image, (self.pos_x, self.pos_y))
            image = self.magic_fight.get_current_image()
            surface.blit(image, (self.pos_x, self.pos_y))
        else:
            image = self.magic_die_escape.get_current_image()
            surface.blit(image, (self.pos_x, self.pos_y))

        pygame.draw.rect(surface, pygame.Color(255, 255, 255), pygame.Rect(self.pos_x, self.pos_y, self.hp / 2, 5))