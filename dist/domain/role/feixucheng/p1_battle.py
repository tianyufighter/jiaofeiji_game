import enum
import pygame
import role


class DiBattleStatus(enum.IntEnum):
    """
    敌人的状态
    """
    Station = 0
    Fight = 1
    Escape = 2
    EscapeOver = 3
    Die = 4
    DieOver = 5


class BattleP1(pygame.sprite.Sprite):
    """
    战斗的敌人
    """
    # 加载死亡行为
    die = role.DirAction("di2\\die", "1152-73d332f0-", 4, 9, False)
    # 加载战斗行为
    fight = role.DirAction("di2\\fight", "1316-85c0b736-", 4, 12, False)
    # 站立行为
    station = role.DirAction("di2\\station", "0517-33f4e27d-", 4, 15, False)
    # 逃跑
    escape = role.Action("magic\\disappear", "0027-760b7bd7-000", 10, False)

    def __init__(self):
        """
        初始化
        """
        pygame.sprite.Sprite.__init__(self)
        self.status = DiBattleStatus.Station
        self.hp = 20
        self.pos_x = 900
        self.pos_y = 400

    def attack_hp(self, hp):
        """
        生命值的改变
        :param hp: 增加或减少的生命值（可正 可负）
        """
        self.hp += hp
        if self.hp <= 0:
            self.set_status(DiBattleStatus.Die)

    def set_status(self, status):
        """
        修改牛魔王的战斗状态
        :param status: 状态值
        """
        self.status = status
        if status == DiBattleStatus.Fight:
            self.fight.reset()
        elif status == DiBattleStatus.Die:
            self.die.reset()
        elif status == DiBattleStatus.Station:
            self.station.reset()
        # elif status == DiBattleStatus.Escape:
        #     self.escape.reset()

    def action_over(self) -> bool:
        """
        判断一个行为是否结束
        :return: 是否结束
        """
        if self.status == DiBattleStatus.Fight:
            return self.fight.is_end()
        elif self.status == DiBattleStatus.Die:
            if self.die.is_end():
                self.status = DiBattleStatus.DieOver
            return self.die.is_end()
        elif self.status == DiBattleStatus.Station:
            return self.station.is_end()
        elif self.status == DiBattleStatus.Escape:
            if self.escape.is_end():
                self.status = DiBattleStatus.EscapeOver
            return self.escape.is_end()

    def draw(self, surface: pygame.Surface):
        """
        绘制函数
        :param surface: 背景图片
        """
        dir = 2
        if self.status == DiBattleStatus.Station:
            image = self.station.get_current_image(dir)
        elif self.status == DiBattleStatus.Fight:
            image = self.fight.get_current_image(dir)
        elif self.status == DiBattleStatus.Die:
            image = self.die.get_current_image(dir)
        elif self.status == DiBattleStatus.DieOver:
            image = self.die.get_current_image(dir)
        # elif self.status == DiBattleStatus.Escape:
        #     image = self.escape.get_current_image()
        # elif self.status == DiBattleStatus.EscapeOver:
        #     image = self.escape.get_current_image()

        if image:
            pygame.draw.rect(surface, pygame.Color(255, 255, 255),pygame.Rect(900, 450, self.hp / 2, 5))
            surface.blit(image, (self.pos_x, self.pos_y))