"""
主函数
初始化pygame
运行场景
退出pygame
"""
import os
import sys

import pygame

from map import SceneResult
from map.bolaicheng_scene import BoLaiChengScene
from map.feixucheng_scene import FeiXuChengScene
from map.huanggong_scene import HuangGongScene
from map.luanyangdian_scene import LuanYangDianScene
from map.start_scene import StartScene
from map.win_fail_scene import WinFailScene
from map.wuzhuangguan_scene import WuZhuangGuanScene

from role.jiang import Jiang


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    pygame.display.set_caption('剿匪记')
    icon_path = os.path.join('resource', 'img', 'icon', '1.png')
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    start_scene = StartScene()
    start_scene.run(screen)
    jiang = Jiang()
    # scene_list = ['HuangGongScene', 'LuanYangDianScene', 'BoLaiChengScene', 'WuZhuangGuanScene', 'FeiXuChengScene', 'HuangGongScene']
    scene_list = ['HuangGongScene', 'HuangGongScene']
    for item in scene_list:
        # 根据类的字符串名称来创建对象
        item_scene = globals()[item](screen, jiang)
        item_scene.run()
        if item_scene.scene_result == SceneResult.Fail:
            final_result = SceneResult.Fail
            break
        if item_scene.scene_result == SceneResult.Win:
            final_result = SceneResult.Win
            break
        if item_scene.scene_result == SceneResult.Quit:
            final_result = SceneResult.Fail
            break
    # 赢和失败的场景
    win_fail_scene = WinFailScene(final_result)
    win_fail_scene.run(screen)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

