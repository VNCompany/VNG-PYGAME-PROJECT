import pygame


class Blackhole(pygame.sprite.Sprite):
    def __init__(self, image, group):
        super(Blackhole, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.y = (500 - self.rect.height) // 2
        self.rect.x = 1000 + self.rect.width

    def update(self):
        if 800 - (self.rect.x + self.rect.width) < 40:
            self.rect = self.rect.move(-8, 0)
