import pygame


class Meteorite(pygame.sprite.Sprite):
    is_alive = True

    def __init__(self, image, group, xy: tuple):
        super(Meteorite, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = xy[0]
        self.rect.y = xy[1]

    def update(self):
        self.rect = self.rect.move(-3, 0)
        if self.rect.x < -150:
            self.kill()
