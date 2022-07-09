# -----------------dimensions of window in pixels--------------------
WIDTH = 800
HEIGHT = 600
WIDTH_SIDEBAR = 200

STEPS_PER_SECOND = 25                   # x updates per second
CHECK_STUCK_ANTS = 5                    # ever x seconds
COORDS_NEST = (WIDTH / 2, HEIGHT / 2)

# ---------------------ant/ cookie parameters------------------------
NUM_START_ANTS = 2
NUM_START_COOKIES = 1

MAX_NUM_ANTS = 100
MAX_NUM_COOKIES = 10

NEW_ANT_CREATION_FREQUENCY = 1      # every x seconds
NEW_COOKIE_CREATION_FREQUENCY = 3   # every x seconds

MIN_SIZE_COOKIE = 3
MAX_SIZE_COOKIE = 5

ANT_VELOCITY = 4                    # in pixels
CARRING_VELOCITY = 1                # in pixels

LENGTH_TRAIL = 30

# ------------------------------colors-------------------------------
WHITE = (255, 255, 255)         # primer
LIGHTGREY = (200, 200,200)      # sidebar

BLACK = (0, 0, 0)               # ant
BLUE = (0, 0, 255)              # ant following
GREEN = (30, 224, 33)           # ant trail

BROWN = (120, 30, 0)            # cookies
LIGHTGREEN = (200, 255, 200)    # cookie attraction area

LIGHTBLUE = (60, 60, 250)       # nest


CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
RED =  (255, 0, 0)
PURPLE = (153, 0, 153)
