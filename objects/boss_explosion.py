import pygame


class BossExplosion(pygame.sprite.Sprite):
    counter = 0

    def __init__(self, image_list: list, group, boss_xy: tuple):
        super(BossExplosion, self).__init__(group)
        self.image_list = image_list
        self.image = self.image_list.pop(0)
        self.rect = self.image.get_rect()
        self.rect.x = boss_xy[0] + 100
        self.rect.y = boss_xy[1] + 100

    def update(self):
        if len(self.image_list) > 0:
            if self.counter == 1:
                self.image = self.image_list.pop(0)
                self.counter = 0
            else:
                self.counter += 0.5
        else:
            self.kill()
