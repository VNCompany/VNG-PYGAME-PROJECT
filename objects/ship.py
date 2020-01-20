import pygame
from defines import WIDTH, HEIGHT


class Ship(pygame.sprite.Sprite):
    is_alive = True

    def __init__(self, image, image_crash, group):
        super(Ship, self).__init__(group)
        self.image = image
        self.image_crash = image_crash
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = 200
        self.rect.y = 250

    def transfer(self, move: str):
        if not self.is_alive:
            return

        if move == "left":
            if self.rect.x >= 5:
                self.rect = self.rect.move(-7, 0)
        if move == "right":
            if self.rect.x + self.rect.width <= WIDTH - 5:
                self.rect = self.rect.move(7, 0)
        if move == "up":
            if self.rect.y >= 5:
                self.rect = self.rect.move(0, -7)
        if move == "down":
            if self.rect.y + self.rect.height <= HEIGHT - 5:
                self.rect = self.rect.move(0, 7)

    def crash(self):
        self.image = self.image_crash
        self.is_alive = False
