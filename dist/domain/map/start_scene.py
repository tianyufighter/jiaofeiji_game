import pygame
from pygame.constants import QUIT, MOUSEBUTTONDOWN


class StartScene:
    """
    结束场景（成功 失败）
    """
    def __init__(self):
        image = pygame.image.load("resource/img/ditu/start.png")
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
                    if 20 < x < 500:
                        if 20 < y < 500:
                            exit = True
            surface.blit(self.image, (0, 0))
            clock.tick(10)
            pygame.display.update()
