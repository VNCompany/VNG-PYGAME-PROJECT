import random
import pygame
from defines import *
from includes import *
from characters_generator import characters_generator
from ini_worker import INI

from objects.win_and_lose import ResScreen
from objects.level import Level
from objects.boss_explosion import BossExplosion

from objects.ship import Ship
from objects.laser import Laser, EnemyLaser
from objects.enemy import Enemy
from objects.meteorite import Meteorite
from objects.blackhole import Blackhole
from objects.boss import Boss

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(WINDOW_TITLE)

random.shuffle(IMAGE_MAPS)

clock = pygame.time.Clock()
SCORE = 0
EVENT_TIMER_INFINITY = pygame.USEREVENT + 1
EVENT_TIMER_BOSSFIRE = EVENT_TIMER_INFINITY + 1

INDICATOR = load_indicator()

# Sound files
if SOUND:
    wav_explosion = pygame.mixer.Sound("data/sound/explosion.wav")
    wav_explosion_boss = pygame.mixer.Sound("data/sound/explosion_boss.wav")
    wav_laser = pygame.mixer.Sound("data/sound/laser.wav")
    wav_teleportation = pygame.mixer.Sound("data/sound/teleportation.wav")
    wav_boss_kick = pygame.mixer.Sound("data/sound/boss_kick.wav")

    wav_laser.set_volume(0.5)
    wav_teleportation.set_volume(0.7)
    wav_boss_kick.set_volume(0.5)
else:
    wav_explosion = None
    wav_explosion_boss = None
    wav_laser = None
    wav_teleportation = None
    wav_boss_kick = None
mp3_start_sound = "data/sound/start_sound.mp3"
mp3_background = "data/sound/background.mp3"
mp3_boss_sound = "data/sound/boss_sound_01.mp3"

# Image files
win_scr = ResScreen(load_image("sprites/bg_win.jpg"), 28)
lose_scr = ResScreen(load_image("sprites/bg_lose.jpg"))
background = load_image("images/background.jpg")
main_manu_background = load_image("images/main_menu.png")

# Sprites
s_ship = load_image("sprites/spaceship1.png")
s_enemy_ships = [
    load_image("sprites/spaceship2.png"),
    load_image("sprites/spaceship2.2.png"),
    load_image("sprites/spaceship2.3.png"),
    load_image("sprites/spaceship2.4.png")
]
s_boss_ship = load_image("sprites/spaceship3.png")
s_meteorite = load_image("sprites/meteorite.png")

s_laser = pygame.transform.scale(load_image("sprites/laser.png"), (50, 10))
s_blue_laser = pygame.transform.scale(load_image("sprites/blue_laser.png"), (105, 25))
s_explosion = load_image("sprites/explosion.png")
s_blackhole = load_image("sprites/blackhole.png")

s_sound_icons = load_sound_icons()


def set_win():
    screen.blit(win_scr.image, win_scr.xy)
    win_scr.update()


def set_lose():
    screen.blit(lose_scr.image, lose_scr.xy)
    lose_scr.update()


def set_score(score: int):
    font = pygame.font.Font(None, 30)
    pause_text = font.render("Score: " + str(score), 1, (255, 255, 0))
    pt_rect = pause_text.get_rect()
    pt_rect.x = 640
    pt_rect.y = 3
    screen.blit(pause_text, pt_rect)


def set_boss_hp(current: int, max: int):
    font = pygame.font.Font(None, 30)
    pause_text = font.render("Boss: " + str(round(current / max * 100)), 1, (255, 255, 0))
    pt_rect = pause_text.get_rect()
    pt_rect.x = 3
    pt_rect.y = 3
    screen.blit(pause_text, pt_rect)


selected_levels = LEVELS_LIST[0]

if SOUND:
    pygame.mixer.music.load(mp3_start_sound)
    pygame.mixer.music.play(start=0.6, loops=-1)

# MAIN MENU
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            terminate()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sound_image_pos = s_sound_icons[0].get_rect()
            sound_image_pos = (736, 15, sound_image_pos.width, sound_image_pos.height)

            if mouse_in_rect(event.pos, pygame.Rect(sound_image_pos)):
                SOUND = not SOUND
                if not SOUND:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            #  Easy
            elif mouse_in_rect(event.pos, pygame.Rect(285, 232, 230, 36)):
                running = False

            #  Normal
            elif mouse_in_rect(event.pos, pygame.Rect(285, 289, 230, 36)):
                selected_levels = LEVELS_LIST[1]
                running = False

            #  Hard
            elif mouse_in_rect(event.pos, pygame.Rect(285, 345, 230, 36)):
                selected_levels = LEVELS_LIST[2]
                running = False

            #  Infinity
            elif mouse_in_rect(event.pos, pygame.Rect(285, 400, 230, 36)):
                selected_levels = LEVELS_LIST[3]
                running = False

    screen.blit(main_manu_background, (0, 0))
    screen.blit(s_sound_icons[0] if SOUND else s_sound_icons[1], (736, 15))

    pygame.display.flip()
    clock.tick(FPS)

# Levels
levels = []
ini_levels = INI.ini_parse(selected_levels)

for i, section in enumerate(ini_levels.get_sections()):
    i_m_prob = float(ini_levels.get(section, "m_prob"))
    i_enemy_count = int(ini_levels.get(section, "enemy_count"))
    i_enemy_speeds = list(ini_levels.get(section, "enemy_speeds"))
    i_enemy_healths = list(ini_levels.get(section, "enemy_healths"))
    i_is_boss_level = ini_levels.get(section, "is_boss_level") == "1"
    lvl = Level(i + 1,
                IMAGE_MAPS[i] if not i_is_boss_level else BOSS_MAP,
                i_m_prob,
                i_enemy_count,
                i_is_boss_level,
                [int(v) for v in i_enemy_speeds],
                i_enemy_healths)

    if section == "Infinity":
        lvl.infinity = True

    if i_is_boss_level:
        val = ini_levels.get(section, "boss_hp")
        i_boss_fire_ms = ini_levels.get(section, "boss_fire_ms")
        if val is not None:
            lvl.boss_hp = int(val)
        if i_boss_fire_ms is not None:
            lvl.boss_fire_ms = int(i_boss_fire_ms)
    levels.append(lvl)

if len(sys.argv) == 2:
    levels = list(filter(lambda t: str(t.id) == str(sys.argv[1]), levels))

screen_start(TITLE_TEXT, screen, clock, FPS)
if SOUND:
    pygame.mixer.music.stop()

    pygame.mixer.music.load(mp3_background)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

# Groups
player_group = pygame.sprite.Group()
player = Ship(s_ship, s_explosion, player_group)  # Main player

laser_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

blackhole_group = pygame.sprite.Group()

boss_group = pygame.sprite.Group()
boss_explosion_group = pygame.sprite.Group()
boss_laser_group = pygame.sprite.Group()


# def generate_enemies(count: int, q: int, speed=3):
#     start_pos = 800
#     end_pos = 50 * count + start_pos
#
#     for i in range(count):
#         if random.randint(1, q) == 2:
#             Meteorite(s_meteorite,
#                       enemy_group,
#                       (random.randrange(start_pos, end_pos), random.randrange(0, 395)),
#                       speed)
#         else:
#             Enemy(s_enemy_ship,
#                   s_explosion,
#                   enemy_group,
#                   (random.randrange(start_pos, end_pos), random.randrange(0, 395)),
#                   speed)


def generate_enemies(count: int, m_prob: float, healths: list, speeds: list):
    points = characters_generator(count, m_prob, (101, 101))

    for point in points:
        if len(speeds) == 0:
            speeds.append(3)
        if point[2] == "m":
            Meteorite(s_meteorite,
                      enemy_group,
                      (point[0], point[1]),
                      random.choice(speeds))
        else:
            if len(healths) == 0:
                healths.append("1:1")
            healths_ints = [int(h.split(":")[0]) for h in healths]
            c = 0
            if len(healths_ints) > 1:
                c = random.randrange(0, len(healths_ints))
            health, score = [int(v) for v in healths[c].split(":")]

            if health == 1:
                s_enemy_ship = s_enemy_ships[0]
            elif health == 2:
                s_enemy_ship = s_enemy_ships[1]
            elif health == 3:
                s_enemy_ship = s_enemy_ships[2]
            elif health >= 4:
                s_enemy_ship = s_enemy_ships[3]
            else:
                s_enemy_ship = s_enemy_ships[0]

            Enemy(s_enemy_ship,
                  s_explosion,
                  enemy_group,
                  (point[0], point[1]),
                  INDICATOR,
                  random.choice(speeds),
                  health,
                  score)


status = G_STATUS_PLAYING


def load_level(lvl: Level):
    global status, SCORE
    generate_enemies(lvl.enemy, lvl.m_prob, lvl.enemy_healths, lvl.enemy_speeds)
    slider_pos_x = 0
    status = G_STATUS_STOPPED

    boss = None
    b_explosion = None
    if lvl.is_boss_level:
        boss = Boss(s_boss_ship, boss_group)
        boss.hp = lvl.boss_hp
        b_explosion = BossExplosion([load_image(img) for img in EXPLOSION_IMAGE_LIST],
                                    boss_explosion_group, (boss.rect.x, boss.rect.y))

    if lvl.infinity:
        pygame.time.set_timer(EVENT_TIMER_INFINITY, 21000)
    if lvl.is_boss_level:
        pygame.time.set_timer(EVENT_TIMER_BOSSFIRE, lvl.boss_fire_ms)

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
                        if SOUND:
                            pygame.mixer.music.pause()
                    elif status == G_STATUS_PAUSE:
                        status = G_STATUS_PLAYING
                        if SOUND:
                            pygame.mixer.music.unpause()
            if e.type == EVENT_TIMER_INFINITY:
                generate_enemies(lvl.enemy, lvl.m_prob, lvl.enemy_healths, lvl.enemy_speeds)
            if e.type == EVENT_TIMER_BOSSFIRE and lvl.is_boss_level and boss.hp > 0:
                EnemyLaser(s_blue_laser, boss_laser_group, boss.rect)
                if SOUND:
                    wav_laser.play()

            if status == G_STATUS_GAMEOVER or status == G_STATUS_WIN:
                if e.type == pygame.KEYDOWN and e.key == 13:
                    running = False

            if status == G_STATUS_PLAYING:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    Laser(s_laser, laser_group, player.rect)
                    if SOUND:
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
        laser_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        boss_laser_group.draw(screen)
        if lvl.is_boss_level:
            boss_group.draw(screen)

        # Action elements
        if status == G_STATUS_PLAYING:
            enemy_group.update()
            laser_group.update()
            boss_laser_group.update()
            if lvl.is_boss_level:
                boss_group.update()

            for enemy in enemy_group:
                for laser in laser_group:
                    if pygame.sprite.collide_mask(laser, enemy):
                        laser.kill()
                        if type(enemy).__name__ == "Enemy":
                            SCORE += enemy.kick()

                if pygame.sprite.collide_mask(player, enemy) and \
                        type(enemy).__name__ != "Indicator":
                    player.crash()
                    if type(enemy).__name__ == "Enemy":
                        enemy.crash()
                        pass
                    if SOUND:
                        wav_explosion.play()
                    status = G_STATUS_GAMEOVER

            if lvl.is_boss_level:
                if boss.hp > 0:
                    for laser in laser_group:
                        for boss_laser in boss_laser_group:
                            if pygame.sprite.collide_mask(laser, boss_laser):
                                laser.kill()
                                boss_laser.kill()

                        if pygame.sprite.collide_mask(laser, boss):
                            laser.kill()
                            laser_y = laser.rect.y
                            laser_yh = laser_y + laser.rect.height
                            if laser_y >= 211 and laser_yh <= 288:
                                boss.kick()
                                if SOUND:
                                    wav_boss_kick.play()

                    for boss_laser in boss_laser_group:
                        if pygame.sprite.collide_mask(boss_laser, player):
                            player.crash()
                            if SOUND:
                                wav_explosion.play()
                            status = G_STATUS_GAMEOVER

                    if pygame.sprite.collide_mask(player, boss):
                        player.crash()
                        if SOUND:
                            wav_explosion.play()
                        status = G_STATUS_GAMEOVER
                if boss.hp == 0:
                    boss.kill()
                    if SOUND:
                        wav_explosion_boss.play()
                    SCORE += 100
                    boss.hp = -1

                if boss.hp == -1:
                    boss_explosion_group.draw(screen)
                    b_explosion.rect.x = boss.rect.x + 100
                    b_explosion.rect.y = boss.rect.y + 100
                    boss_explosion_group.update()

        set_score(SCORE)
        if lvl.is_boss_level and status == G_STATUS_PLAYING and boss.hp != -1:
            set_boss_hp(boss.hp, lvl.boss_hp)

        if status == G_STATUS_GAMEOVER:
            if lvl.infinity:
                pygame.time.set_timer(EVENT_TIMER_INFINITY, 0)
            pygame.time.set_timer(EVENT_TIMER_BOSSFIRE, 0)
            set_lose()
        elif status == G_STATUS_WIN:
            set_win()

        if len(enemy_group) == 0:
            if lvl.id == 6:
                if len(boss_explosion_group) == 0:
                    status = G_STATUS_WIN
            elif not lvl.infinity:
                blackhole_group.draw(screen)
                blackhole_group.update()

                for blackhole in blackhole_group:
                    if pygame.sprite.collide_mask(player, blackhole):
                        if SOUND:
                            wav_teleportation.play()
                        return
            else:
                pass

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
    if level.is_boss_level and SOUND:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(mp3_boss_sound)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
    load_level(level)

    # Closing level
    player.rect.x = 100
    player.rect.y = 150
    blackhole_group.empty()

    if status != G_STATUS_PLAYING:
        level_count = level.id - 1
        if SOUND:
            pygame.mixer.music.stop()
        break

if status == G_STATUS_WIN:
    level_count = 6

if SOUND:
    pygame.mixer.music.load(mp3_start_sound)
    pygame.mixer.music.play(start=0.6, loops=-1)
score_screen(SCORE_TEXT, screen, clock, FPS, str(SCORE), str(level_count))

pygame.quit()
