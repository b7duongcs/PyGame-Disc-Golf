import pygame
import os

pygame.init()

#display constants
WIDTH, HEIGHT = 1000, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disc Golf")
FPS = 60
TICKS_PER_FRAME = 1000/FPS
TIME_LIMIT = 6000

#colours
GREEN = (0,128,0)
RED = (255,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139,69,19)
GREY = (105,105,105)

#fonts
TIMER_FONT = pygame.font.Font('freesansbold.ttf', 32)
GRAPH_FONT = pygame.font.Font('freesansbold.ttf', 10)
ROTATION_FONT = pygame.font.Font('freesansbold.ttf', 25)
POWER_FONT = pygame.font.Font('freesansbold.ttf', 25)
ROT_TITLE_FONT = pygame.font.Font('freesansbold.ttf', 25)
ANGLE_FONT = pygame.font.Font('freesansbold.ttf', 12)

#adjustment factors
FT_TO_PIXELS = 5
INTERVAL_LEN = 50
BORDER = 10
BAR_THICKNESS = 4
UI_DISTANCE = 50
UI_OFFSET = 225

#disc constants
DISC_SIZE = 32
DISC_IMAGE = pygame.image.load(os.path.join('assets', 'disc_sprite.png'))
DISC = pygame.transform.scale(DISC_IMAGE, (DISC_SIZE, DISC_SIZE))
START_X = BORDER
#START_Y_DEF = (HEIGHT - DISC_SIZE) / 2 #center
START_Y_LOWER = BORDER
START_Y_UPPER = HEIGHT - BORDER - DISC_SIZE

#launch speed
MAX_SPEED = 27 #m/s
PIXELS_PER_MS = 7
PB_X = BORDER + UI_OFFSET
PB_Y = HEIGHT - (MAX_SPEED * PIXELS_PER_MS + BORDER)
PB_WIDTH = 150
PB_HEIGHT = MAX_SPEED * PIXELS_PER_MS
POWER_BAR = pygame.Rect(PB_X, PB_Y, PB_WIDTH, PB_HEIGHT)
POWER_TITLE = POWER_FONT.render("Power", True, WHITE)
POWER_TITLE_Y = HEIGHT - BORDER*2 - POWER_TITLE.get_height()
POWER_TITLE_X = PB_X + (PB_WIDTH - POWER_TITLE.get_width())/2

#rotation
ROT_HEIGHT = 50
ROT_X = PB_X
ROT_Y = PB_Y - ROT_HEIGHT - BORDER
ROT_WIDTH = PB_WIDTH
ROT_BUTTON = pygame.Rect(ROT_X, ROT_Y, ROT_WIDTH, ROT_HEIGHT)
ROT_TITLE = ROT_TITLE_FONT.render("Rotation", True, WHITE)
ROT_TITLE_X = ROT_X + (ROT_WIDTH - ROT_TITLE.get_width())/2
ROT_TITLE_Y = ROT_Y - BORDER - ROT_TITLE.get_height()

COVER_Y = ROT_Y + BAR_THICKNESS
COVER_W = (ROT_WIDTH - 2*BAR_THICKNESS) / 2
COVER_H = ROT_HEIGHT - 2*BAR_THICKNESS
COVER_OFFSET = (ROT_WIDTH - 2*BAR_THICKNESS) / 2

ROT_TEXT_Y = COVER_Y + BORDER

#angle ui constants
LINE_LEN = 100
LINE_THICKNESS = 3
ANGLE_UI_Y = PB_Y
ANGLE_TITLE_Y_OFFSET = 30
POWER_SCALE = 0.2
DEGREE_SCALE = 0.5

#vertical angle
VA_BL_X = PB_X + PB_WIDTH + UI_DISTANCE

#horizontal angle
HA_BL_X = VA_BL_X + LINE_LEN + UI_DISTANCE

#nose angle
NA_BL_X = HA_BL_X + LINE_LEN + UI_DISTANCE

#roll angle
RA_BL_X = NA_BL_X + LINE_LEN + UI_DISTANCE

#xz graph constants
GRAPH_UPPER_Y_BOUND = HEIGHT - 65 - BORDER
GRAPH_LOWER_Y_BOUND = HEIGHT - 15 - BORDER
GRAPH_LOWER_X_BOUND = WIDTH - 215
Z_BAR = pygame.Rect(GRAPH_LOWER_X_BOUND - 2, GRAPH_UPPER_Y_BOUND + 5, 2, 50)
X_BAR = pygame.Rect(GRAPH_LOWER_X_BOUND - 2, GRAPH_LOWER_Y_BOUND + 5, 200, 2)
GRAPH_TITLE_X = GRAPH_LOWER_X_BOUND
GRAPH_TITLE_Y = GRAPH_UPPER_Y_BOUND - 20

#goal and obstacle
GOAL_UPPER_Z = 1.33 * 3.28 #ft
GOAL_LOWER_Z = 0.65 * 3.28 #ft
GOAL_MP_Z = (GOAL_UPPER_Z + GOAL_LOWER_Z) / 2
OBSTACLE_Z = 5  * 3.28 #ft
OBJ_SIZE = 64
OBJ_LOWER_Y = BORDER
OBJ_UPPER_Y = HEIGHT - BORDER - OBJ_SIZE
OBJ_LOWER_X = BORDER + 4*DISC_SIZE
OBJ_UPPER_X = WIDTH - BORDER - OBJ_SIZE