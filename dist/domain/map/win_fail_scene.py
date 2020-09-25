import pygame
from pygame.constants import QUIT, MOUSEBUTTONDOWN

from map import SceneResult


class WinFailScene:
    """
    结束场景（成功 失败）
    """
    def __init__(self, state):
        if state == SceneResult.Win:
            image = pygame.image.load("resource/img/ditu/success.jpeg")
        elif state == SceneResult.Fail:
            image = pygame.image.load("resource/img/ditu/lose.jpeg")
        self.image = pygame.transform.scale(image, (800, 600))

    def run(self, surface):
        clock = pygame.time.Clock()
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit = True
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 0 < x < 800:
                        if 0 < y < 600:
                            exit = True
            surface.blit(self.image, (0, 0))
            clock.tick(10)
            pygame.display.update()
