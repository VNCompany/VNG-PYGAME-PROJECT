import pygame
from defines import *
from includes import *
from objects.win_and_lose import ResScreen

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(WINDOW_TITLE)

clock = pygame.time.Clock()
SCORE = 498

win_scr = ResScreen(load_image("sprites/bg_win.jpg"))
lose_scr = ResScreen(load_image("sprites/bg_lose.jpg"))


def set_win():
    screen.blit(win_scr.image, win_scr.xy)
    win_scr.update()


def set_lose():
    screen.blit(lose_scr.image, lose_scr.xy)
    lose_scr.update()


running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            terminate()
        if e.type == pygame.KEYDOWN or e.type == pygame.MOUSEBUTTONDOWN:
            running = False

    fon = load_image("images/background.jpg")
    screen.blit(fon, (0, 0))

    set_win()

    pygame.display.flip()
    clock.tick(FPS)

score_screen(SCORE_TEXT, screen, clock, FPS, str(SCORE))

pygame.quit()
