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
    font = pygame.font.Font(None, 35)
    txt_pos = 150
    for string in text:
        s = font.render(string, 1, (255, 255, 0))
        s_rect = s.get_rect()
        txt_pos += 15
        s_rect.y = txt_pos
        s_rect.x = 155
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


def score_screen(text: list, screen, clock, fps, score):
    bg = load_image("images/background.jpg")
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 35)
    txt_pos = 190
    for string in text:
        s = font.render(string.replace("{0}", score), 1, (255, 255, 0))
        s_rect = s.get_rect()
        txt_pos += 15
        s_rect.y = txt_pos
        s_rect.x = 250
        txt_pos += s_rect.height
        screen.blit(s, s_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.flip()
        clock.tick(fps)
