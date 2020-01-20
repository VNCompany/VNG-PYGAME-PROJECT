import pygame
from defines import WIDTH, HEIGHT


class Boss(pygame.sprite.Sprite):
    hp = 150

    def __init__(self, image, group):
        super(Boss, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.y = (HEIGHT - self.rect.height) // 2
        self.rect.x = WIDTH

    def update(self):
        if self.hp == 0:
            return

        self.rect = self.rect.move(-1, 0)

    def kick(self):
        self.hp -= 1
