import ini_worker

# Config
cfg = ini_worker.INI.ini_parse("config.ini")

# Constants
G_STATUS_PLAYING = 0
G_STATUS_PAUSE = 1
G_STATUS_WIN = 2
G_STATUS_GAMEOVER = 3
G_STATUS_STOPPED = 4

GENERATION_MOD_OLD = 0
GENERATION_MOD_NEW = 1

SCORE_MAIN_MENU = 0
SCORE_NONE = 1

# Parameters
SIZE = WIDTH, HEIGHT = 800, 500
FPS = int(cfg.get("Default", "fps"))
WINDOW_TITLE = "Warspace"
SOUND = int(cfg.get("Default", "sound")) == 1

GENERATION_MOD = int(cfg.get("Default", "generation_mod"))

TITLE_TEXT = ["--------------------- Control ---------------------",
              "              Keyboard arrows - moving",
              "              SPACE - shooting",
              "              P - Pause",
              "------------------------------------------------------",
              "                      PRESS ANY BUTTON"
              ]

SCORE_TEXT = ["------------------- Results -------------------",
              "    Score: {0}",
              "    Completed levels: {1}",
              "---------------------------------------------------"]

IMAGE_MAPS = [
    "images/planet_1.jpg",
    "images/planet_2.jpg",
    "images/planet_3.jpg",
    "images/planet_4.jpg",
    "images/planet_5.jpg",
]

BOSS_MAP = "images/boss_planet.jpg"

EXPLOSION_IMAGE_LIST = [
    "sprites/explosion_animation/1.png",
    "sprites/explosion_animation/2.png",
    "sprites/explosion_animation/3.png",
    "sprites/explosion_animation/4.png",
    "sprites/explosion_animation/5.png",
    "sprites/explosion_animation/6.png",
    "sprites/explosion_animation/7.png",
    "sprites/explosion_animation/8.png",
    "sprites/explosion_animation/9.png",
    "sprites/explosion_animation/10.png",
    "sprites/explosion_animation/11.png",
    "sprites/explosion_animation/12.png"
]

LEVELS_LIST = [
    "levels/levels_easy.ini",
    "levels/levels_normal.ini",
    "levels/levels_hard.ini",
    "levels/levels_infinity.ini"
]
