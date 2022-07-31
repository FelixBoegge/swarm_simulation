import pygame.image
pygame.init()


# -----------------------------------------dimensions of window in pixels-----------------------------------------
WIDTH = 800
HEIGHT = 600
WIDTH_SIDEBAR = 300

STEPS_PER_SECOND = 25                   # x updates per second
COORDS_NEST = (WIDTH / 2, HEIGHT / 2)

# --------------------------------------------ant/ cookie parameters----------------------------------------------
NUM_START_ANTS = 5
NUM_START_COOKIES = 1

MAX_NUM_ANTS = 100
MAX_NUM_COOKIES = 10

NEW_ANT_CREATION_FREQUENCY = 1          # every x seconds
NEW_COOKIE_CREATION_FREQUENCY = 3       # every x seconds

MIN_SIZE_COOKIE = 5
MAX_SIZE_COOKIE = 20

ANT_VELOCITY = 4                        # in pixels (default value)
CARRING_VELOCITY = 1                    # in pixels

LENGTH_TRAIL = 30

# ---------------------------------------------------colors-------------------------------------------------------
WHITE = (255, 255, 255)                 # primer
LIGHTGREY = (200, 200,200)              # sidebar

GREY = (150, 150, 150)                  # slider bar
GREEN = (30, 224, 33)                   # slider pointer
GREEN2 = (0, 153, 0)                    # stastic values collections
RED =  (255, 0, 0)                      # statistic values killed ants

BLACK = (0, 0, 0)                       # ant
PURPLE = (153, 0, 153)                  # ant trail

DARKGREY = (30, 30, 30)                 # nest

# --------------------------------------------------images--------------------------------------------------------
COOKIE_IMG = pygame.image.load('assets/cookie_img.png')
ANT_IMG = pygame.image.load('assets/ant.png')
BACKGROUND = pygame.transform.scale(pygame.image.load('assets/leaf_background.jpg'), (WIDTH, HEIGHT))
BACKGROUND.set_alpha(190)
ATTRACTION = pygame.image.load('assets/yellow_circle.png')

# --------------------------------------------------fonts---------------------------------------------------------

cookie_val_font = pygame.font.SysFont('Sans Serif', 15)     # occupancy/ size of cookie
slider_label_font = pygame.font.SysFont('Georgia', 14)      # slider labels
slider_val_font = pygame.font.SysFont('Sans Serif', 16)     # numbers on sliders
info_text_font = pygame.font.SysFont('Georgia', 16)         # statistic text
info_val_font = pygame.font.SysFont('Sans Serif', 25)       # statistic values
