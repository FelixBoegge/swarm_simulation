import pygame.image


# -----------------dimensions of window in pixels--------------------
WIDTH = 800
HEIGHT = 600
WIDTH_SIDEBAR = 300

STEPS_PER_SECOND = 25                   # x updates per second
COORDS_NEST = (WIDTH / 2, HEIGHT / 2)

# ---------------------ant/ cookie parameters------------------------
NUM_START_ANTS = 2
NUM_START_COOKIES = 1

MAX_NUM_ANTS = 100
MAX_NUM_COOKIES = 10

NEW_ANT_CREATION_FREQUENCY = 1      # every x seconds
NEW_COOKIE_CREATION_FREQUENCY = 3   # every x seconds

MIN_SIZE_COOKIE = 5
MAX_SIZE_COOKIE = 25

ANT_VELOCITY = 4                    # in pixels (default value)
CARRING_VELOCITY = 1                # in pixels

LENGTH_TRAIL = 30

# ------------------------------colors-------------------------------
WHITE = (255, 255, 255)         # primer
LIGHTGREY = (200, 200,200)      # sidebar

GREY = (150, 150, 150)          # slider bar
GREEN = (30, 224, 33)           # slider pointer

BLACK = (0, 0, 0)               # ant
PURPLE = (153, 0, 153)          # ant trail

DARKGREY = (30, 30, 30)         # nest

# ------------------------------images-------------------------------
COOKIE_IMG = pygame.image.load('assets/cookie_img.png')
BACKGROUND = pygame.transform.scale(pygame.image.load(('assets/leaf_background2.jpg')), (WIDTH, HEIGHT))
ATTRACTION = pygame.image.load('assets/green_circle.png')


CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
RED =  (255, 0, 0)
GREEN = (30, 224, 33)
BLUE = (0, 0, 255)
