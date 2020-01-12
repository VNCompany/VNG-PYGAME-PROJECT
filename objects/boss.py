import pygame


class Boss(pygame.sprite.Sprite):
    hp = 150
    x_pos = 0

    def __init__(self, image, group):
        super(Boss, self).__init__(group)
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.y = 0
        self.rect.x = 800

    def update(self):
        if self.hp == 0:
            return

        self.x_pos += 0.5
        if self.x_pos == 1:
            self.x_pos = 0
            self.rect = self.rect.move(-1, 0)

    def kick(self):
        self.hp -= 1
