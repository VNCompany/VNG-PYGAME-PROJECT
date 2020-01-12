import random
import pygame
from defines import *
from includes import *

from objects.win_and_lose import ResScreen
from objects.level import Level

from objects.ship import Ship
from objects.laser import Laser
from objects.enemy import Enemy
from objects.meteorite import Meteorite
from objects.blackhole import Blackhole

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
background = load_image("images/background.jpg")

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
    Level(1, IMAGE_MAPS[0], 10, 10, False),
    Level(2, IMAGE_MAPS[1], 9, 20, False),
    Level(3, IMAGE_MAPS[2], 8, 25, False),
    Level(4, IMAGE_MAPS[3], 7, 30, False),
    Level(5, IMAGE_MAPS[4], 7, 40, False, 4),
    Level(6, BOSS_MAP, 4, 50, True, 4),
]


def set_win():
    screen.blit(win_scr.image, win_scr.xy)
    win_scr.update()


def set_lose():
    screen.blit(lose_scr.image, lose_scr.xy)
    lose_scr.update()


def set_score(score: int):
    font = pygame.font.Font(None, 30)
    pause_text = font.render("Счёт: " + str(score), 1, (255, 255, 0))
    pt_rect = pause_text.get_rect()
    pt_rect.x = 700
    pt_rect.y = 3
    screen.blit(pause_text, pt_rect)


screen_start(TITLE_TEXT, screen, clock, FPS)

# Groups
player_group = pygame.sprite.Group()
player = Ship(s_ship, s_explosion, player_group)  # Main player

laser_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

blackhole_group = pygame.sprite.Group()


def generate_enemies(count: int, q: int, speed=3):
    start_pos = 1000
    end_pos = 100 * count + start_pos - 200

    for i in range(count):
        if random.randint(1, q) == 2:
            Meteorite(s_meteorite,
                      enemy_group,
                      (random.randint(start_pos, end_pos), random.randint(5, 395)),
                      speed)
        else:
            Enemy(s_enemy_ship,
                  s_explosion,
                  enemy_group,
                  (random.randint(start_pos, end_pos), random.randint(5, 395)),
                  speed)


status = G_STATUS_PLAYING


def load_level(lvl: Level):
    global status, SCORE
    generate_enemies(lvl.enemy, lvl.quality, lvl.enemy_speed)
    slider_pos_x = 0
    status = G_STATUS_STOPPED
    running = True
    while running:
        pressed = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                terminate()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    status = G_STATUS_STOPPED
                if e.key == pygame.K_p:
                    if status == G_STATUS_PLAYING:
                        status = G_STATUS_PAUSE
                    elif status == G_STATUS_PAUSE:
                        status = G_STATUS_PLAYING

            if status == G_STATUS_GAMEOVER or status == G_STATUS_WIN:
                if e.type == pygame.KEYDOWN and e.key == 13:
                    running = False

            if status == G_STATUS_PLAYING:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    Laser(s_laser, laser_group, player.rect)
                    wav_laser.play()

        if status == G_STATUS_PAUSE:
            screen.blit(background, (0, 0))
            font = pygame.font.Font(None, 100)
            pause_text = font.render("ПАУЗА", 1, (255, 255, 0))
            pt_rect = pause_text.get_rect()
            pt_rect.x = 280
            pt_rect.y = 214
            screen.blit(pause_text, pt_rect)

            pygame.display.flip()
            clock.tick(FPS)
            continue

        if status == G_STATUS_PLAYING:
            if pressed[pygame.K_UP]:
                player.transfer('up')
            if pressed[pygame.K_DOWN]:
                player.transfer('down')
            if pressed[pygame.K_LEFT]:
                player.transfer('left')
            if pressed[pygame.K_RIGHT]:
                player.transfer('right')

        screen.blit(load_image(lvl.image), (0, 0))

        # Drawing elements
        player_group.draw(screen)
        laser_group.draw(screen)
        enemy_group.draw(screen)

        # Action elements
        if status == G_STATUS_PLAYING:
            enemy_group.update()
            laser_group.update()

            for enemy in enemy_group:
                for laser in laser_group:
                    if pygame.sprite.collide_mask(laser, enemy):
                        laser.kill()
                        if type(enemy).__name__ != "Meteorite":
                            enemy.kill()
                            SCORE += 1

                if pygame.sprite.collide_mask(player, enemy):
                    player.crash()
                    if type(enemy).__name__ != "Meteorite":
                        enemy.crash()
                    wav_explosion.play()
                    status = G_STATUS_GAMEOVER

        set_score(SCORE)

        if status == G_STATUS_GAMEOVER:
            set_lose()
        elif status == G_STATUS_WIN:
            set_win()

        if len(enemy_group) == 0:
            if lvl.id == 6:
                status = G_STATUS_WIN
            else:
                blackhole_group.draw(screen)
                blackhole_group.update()

                for blackhole in blackhole_group:
                    if pygame.sprite.collide_mask(player, blackhole):
                        wav_teleportation.play()
                        return

        if -1 < slider_pos_x < 800:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(slider_pos_x, 0, 800, 500))
            slider_pos_x += 50
        elif slider_pos_x != -1:
            slider_pos_x = -1
            status = G_STATUS_PLAYING

        pygame.display.flip()
        clock.tick(FPS)


level_count = 0
for level in levels:
    Blackhole(s_blackhole, blackhole_group)

    load_level(level)

    # Closing level
    player.rect.x = 100
    player.rect.y = 150
    blackhole_group.empty()

    if status != G_STATUS_PLAYING:
        level_count = level.id - 1
        break

score_screen(SCORE_TEXT, screen, clock, FPS, str(SCORE), str(level_count))

pygame.quit()
