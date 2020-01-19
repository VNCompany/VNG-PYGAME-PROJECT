import pygame
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def screen_start(text: list, screen, clock, fps):
    bg = load_image("images/background.jpg")
    screen.blit(bg, (0, 0))
    font = pygame.font.Font("data/fonts/impact.ttf", 35)
    txt_pos = 100
    for string in text:
        s = font.render(string, 1, (255, 255, 0))
        s_rect = s.get_rect()
        txt_pos += 10
        s_rect.y = txt_pos
        s_rect.x = 116
        txt_pos += s_rect.height
        screen.blit(s, s_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def score_screen(text: list, screen, clock, fps, score, level_count):
    close_status = 1
    bg = load_image("images/score.png")
    screen.blit(bg, (0, 0))
    font = pygame.font.Font("data/fonts/RobotoMono.ttf", 35)
    txt_pos = 90
    text.sort(reverse=True)
    if len(text) > 7:
        text = text[:7]
    for i, string in enumerate(text):
        string = str(string)
        dots = "............."
        if len(string) + 1 < 21:
            dots = '.' * (21 - (len(string) + 1))
        res = str(i + 1) + dots + string
        s = font.render(res,
                        1, (255, 255, 0))
        s_rect = s.get_rect()
        txt_pos += 2
        s_rect.y = txt_pos
        s_rect.x = 178
        txt_pos += s_rect.height
        screen.blit(s, s_rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    pygame.mixer.music.stop()
                except:
                    print("У вас проблемы с аудио системой.")
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_in_rect(event.pos, pygame.Rect(529, 435, 57, 42)):
                    close_status = 1
                    running = False
                elif mouse_in_rect(event.pos, pygame.Rect(209, 435, 158, 42)):
                    close_status = 0
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close_status = 1
                    running = False
                elif event.key == pygame.K_m:
                    close_status = 0
                    running = False
        pygame.display.flip()
        clock.tick(fps)
    return close_status


def load_indicator():
    full_image = load_image("sprites/indicator.png")

    values = [10, 20, 30, 50, 60, 80, 100]

    indicator_dict = {}

    for i in range(7):
        sub_image = full_image.subsurface(pygame.Rect((41 * i, 0), (41, 6)))
        indicator_dict[values[i]] = sub_image
    return indicator_dict


def load_sound_icons():
    full_image = load_image("sprites/sound.png")

    img1 = full_image.subsurface(pygame.Rect(0, 0, 46, 28))
    img2 = full_image.subsurface(pygame.Rect(48, 0, 46, 28))

    return img1, img2


def mouse_in_rect(mouse_xy: tuple, rect: pygame.Rect):
    return rect.collidepoint(mouse_xy[0], mouse_xy[1])
