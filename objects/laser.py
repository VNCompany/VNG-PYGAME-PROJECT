import pygame
from defines import WIDTH, HEIGHT


class Laser(pygame.sprite.Sprite):
    def __init__(self, image, group, ship_rect: pygame.Rect):
        super(Laser, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = ship_rect.x + ship_rect.width - self.rect.width + 10
        self.rect.y = ship_rect.y + 20

    def update(self):
        self.rect = self.rect.move(17, 0)
        if self.rect.x + self.rect.width > WIDTH:
            self.kill()


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, image, group, ship_rect: pygame.Rect):
        super(EnemyLaser, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = ship_rect.x + 2 + self.rect.width
        self.rect.y = (HEIGHT - self.rect.height) // 2

    def update(self):
        self.rect = self.rect.move(-19, 0)
        if self.rect.x + self.rect.width < -5:
            self.kill()
