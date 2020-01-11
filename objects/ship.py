import pygame


class Ship(pygame.sprite.Sprite):
    is_alive = True

    def __init__(self, image, image_crash, group):
        super(Ship, self).__init__(group)
        self.image = image
        self.image_crash = image_crash
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = 100
        self.rect.y = 150

    def transfer(self, move: str):
        if not self.is_alive:
            return

        if move == "left":
            if self.rect.x >= 5:
                self.rect = self.rect.move(-5, 0)
        if move == "right":
            if self.rect.x + self.rect.width <= 795:
                self.rect = self.rect.move(5, 0)
        if move == "up":
            if self.rect.y >= 5:
                self.rect = self.rect.move(0, -5)
        if move == "down":
            if self.rect.y + self.rect.height <= 495:
                self.rect = self.rect.move(0, 5)

    def crash(self):
        self.image = self.image_crash
        self.is_alive = False
