import pygame
from defines import WIDTH


class Blackhole(pygame.sprite.Sprite):
    def __init__(self, image, group):
        super(Blackhole, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.y = (WIDTH - self.rect.height) // 2
        self.rect.x = WIDTH + 100 + self.rect.width

    def update(self):
        if WIDTH - (self.rect.x + self.rect.width) < 20:
            self.rect = self.rect.move(-10, 0)
