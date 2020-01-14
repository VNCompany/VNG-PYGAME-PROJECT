import pygame


class Indicator(pygame.sprite.Sprite):
    def __init__(self, group, xy: tuple, indicator_image, value=100):
        super(Indicator, self).__init__(group)
        self.i_image = indicator_image
        self.image = self.i_image[value]
        self.rect = self.image.get_rect()
        self.rect.x = xy[0] + 26
        self.rect.y = xy[1] - 11

    def transfer(self, xy: tuple):
        self.rect.x = xy[0] + 26
        self.rect.y = xy[1] - 11

    def set_value(self, percent: int):
        self.image = self.i_image[percent]
        pass


class Enemy(pygame.sprite.Sprite):
    is_alive = True

    def __init__(self, image,
                 image_crash,
                 group, xy: tuple,
                 indicator_image,
                 speed=3,
                 health=1,
                 score=1):
        super(Enemy, self).__init__(group)
        self.image = image
        self.image_crash = image_crash
        self.mask = pygame.mask.from_surface(image)
        self.rect = image.get_rect()
        self.rect.x = xy[0]
        self.rect.y = xy[1]
        self.speed = speed

        self.hp = health
        self.HEALTH = health
        self.score = score
        if health > 1:
            self.indicator = Indicator(group, (self.rect.x, self.rect.y), indicator_image)

    def update(self):
        if not self.is_alive:
            return

        self.rect = self.rect.move(-self.speed, 0)
        if self.HEALTH > 1:
            self.indicator.transfer((self.rect.x, self.rect.y))
        if self.rect.x < -150:
            if self.HEALTH > 1:
                self.indicator.kill()
            self.kill()

    def kick(self):
        self.hp -= 1

        if self.HEALTH > 1:
            percent = int(round(self.hp / self.HEALTH * 100))

            if 0 < percent < 20:
                self.indicator.set_value(10)
            elif 20 <= percent < 30:
                self.indicator.set_value(20)
            elif 30 <= percent < 50:
                self.indicator.set_value(30)
            elif 50 <= percent < 60:
                self.indicator.set_value(50)
            elif 60 <= percent < 80:
                self.indicator.set_value(60)
            elif 80 <= percent < 100:
                self.indicator.set_value(80)
            elif percent == 100:
                self.indicator.set_value(100)

        if self.hp <= 0:
            if self.HEALTH > 1:
                self.indicator.kill()
            self.kill()
            return self.score
        return 0

    def crash(self):
        self.image = self.image_crash
        self.is_alive = False
