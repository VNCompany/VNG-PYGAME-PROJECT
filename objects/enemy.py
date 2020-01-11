import pygame


class Enemy(pygame.sprite.Sprite):
    is_alive = True

    def __init__(self, image, image_crash, group, xy: tuple):
        super(Enemy, self).__init__(group)
        self.image = image
        self.image_crash = image_crash
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = xy[0]
        self.rect.y = xy[1]

    def update(self):
        if not self.is_alive:
            return

        self.rect = self.rect.move(-3, 0)
        if self.rect.x < -150:
            self.kill()

    def crash(self):
        self.image = self.image_crash
        self.is_alive = False
