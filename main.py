import random
import pygame
from defines import *
from includes import *

from objects.win_and_lose import ResScreen
from objects.level import Level

from objects.ship import Ship
from objects.laser import Laser

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(WINDOW_TITLE)

random.shuffle(IMAGE_MAPS)

clock = pygame.time.Clock()
SCORE = 0

# Sound files
wav_explosion = pygame.mixer.Sound("data/sound/explosion.wav")
wav_explosion_boss = pygame.mixer.Sound("data/sound/explosion_boss.wav")
wav_laser = pygame.mixer.Sound("data/sound/laser.wav")
wav_teleportation = pygame.mixer.Sound("data/sound/teleportation.wav")

# Image files
win_scr = ResScreen(load_image("sprites/bg_win.jpg"))
lose_scr = ResScreen(load_image("sprites/bg_lose.jpg"))

# Sprites
s_ship = load_image("sprites/spaceship1.png")
s_enemy_ship = load_image("sprites/spaceship2.png")
s_boss_ship = load_image("sprites/spaceship1.png")
s_meteorite = load_image("sprites/meteorite.png")

s_laser = pygame.transform.scale(load_image("sprites/laser.png"), (50, 10))
s_explosion = load_image("sprites/explosion.png")
s_blackhole = load_image("sprites/blackhole.png")

# Levels
levels = [
    Level(1, IMAGE_MAPS[0], 1, 20, False),
    Level(2, IMAGE_MAPS[1], 2, 20, False),
    Level(3, IMAGE_MAPS[2], 3, 20, False),
    Level(4, IMAGE_MAPS[3], 4, 20, False),
    Level(5, IMAGE_MAPS[4], 5, 20, False),
    Level(6, BOSS_MAP, 6, 20, True),
]


def set_win():
    screen.blit(win_scr.image, win_scr.xy)
    win_scr.update()


def set_lose():
    screen.blit(lose_scr.image, lose_scr.xy)
    lose_scr.update()


screen_start(TITLE_TEXT, screen, clock, FPS)

# Groups
player_group = pygame.sprite.Group()
player = Ship(s_ship, s_explosion, player_group)  # Main player

laser_group = pygame.sprite.Group()

# for level in levels:
running = True
while running:
    pressed = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            terminate()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            Laser(s_laser, laser_group, player.rect)
            wav_laser.play()

    if pressed[pygame.K_UP]:
        player.transfer('up')
    if pressed[pygame.K_DOWN]:
        player.transfer('down')
    if pressed[pygame.K_LEFT]:
        player.transfer('left')
    if pressed[pygame.K_RIGHT]:
        player.transfer('right')

    screen.blit(load_image(levels[0].image), (0, 0))

    player_group.draw(screen)
    laser_group.draw(screen)
    laser_group.update()

    pygame.display.flip()
    clock.tick(FPS)

score_screen(SCORE_TEXT, screen, clock, FPS, str(SCORE))

pygame.quit()
