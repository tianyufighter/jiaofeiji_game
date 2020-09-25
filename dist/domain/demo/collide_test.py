import pygame


class Triangle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Triangle, self).__init__()
        self.image = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 100, 240),[(60, 0), (120, 120), (0, 120)])
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


class Circle1(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Circle1, self).__init__()
        self.image = pygame.Surface((120,120), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (204, 255, 153), (60, 60), 60)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


class Circle2(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Circle2, self).__init__()
        self.image = pygame.Surface((120,120), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 153, 204), (60, 60), 60)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)


class Circle3(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Circle3, self).__init__()
        self.image = pygame.Surface((120,120), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (244, 0, 51), (60, 60), 60)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

class Square(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Square, self).__init__()
        self.image = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 153), ((20, 20), (20, 20)), 0)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
triangle = Triangle((20, 20))
circle1 = Circle1((100, 59))
circle2 = Circle2((204, 340))
circle3 = Circle3((809, 240))
square = Square((400, 502))
all_sprites = pygame.sprite.Group(triangle, circle1, circle2, circle3, square)
done = False

clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEMOTION:
            triangle.rect.center = event.pos
    if pygame.sprite.collide_circle(triangle, circle1):
        pygame.display.set_caption('collision')
    elif pygame.sprite.collide_circle(triangle, circle2):
        pygame.display.set_caption('collision')
    elif pygame.sprite.collide_circle(triangle, circle3):
        pygame.display.set_caption('collision')
    elif pygame.sprite.collide_circle(triangle, square):
        pygame.display.set_caption('collision')
    else:
        pygame.display.set_caption("no collision")
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()