import pygame


class Meteorite(pygame.sprite.Sprite):
    def __init__(self, image, group, xy: tuple, speed=3):
        super(Meteorite, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = xy[0]
        self.rect.y = xy[1]
        self.speed = speed

    def update(self):
        self.rect = self.rect.move(-self.speed, 0)
        if self.rect.x < -150:
            self.kill()
