import pygame
import os
import random
from disc_flight import *
from parameters import *

pygame.init()

#display constants
WIDTH, HEIGHT = 1000, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disc Golf")
FPS = 60
TICKS_PER_FRAME = 1000/FPS
TIME_LIMIT = 10000

#colours
GREEN = (0,128,0)
RED = (255,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (220,220,220)
BROWN = (139,69,19)
YELLOW = (255,255,0)

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
GOAL_UPPER_Z = 1.33 #m
GOAL_LOWER_Z =  0.65 #m
OBSTACLE_Z = 5 #m
OBJ_SIZE = 64
OBJ_LOWER_Y = BORDER
OBJ_UPPER_Y = HEIGHT - BORDER - OBJ_SIZE
OBJ_LOWER_X = BORDER + 4*DISC_SIZE
OBJ_UPPER_X = WIDTH - BORDER - OBJ_SIZE

def draw_angle_ui(x, angle, title):
    mp_y = ANGLE_UI_Y + PB_HEIGHT/2
    angle_x = LINE_LEN * np.cos(np.radians(angle))
    angle_y = LINE_LEN * np.sin(np.radians(angle))

    text = ANGLE_FONT.render(title, True, WHITE)
    WIN.blit(text, (x + (LINE_LEN - text.get_width())/2, ANGLE_UI_Y - ANGLE_TITLE_Y_OFFSET))

    pygame.draw.line(WIN, BLACK, (x, ANGLE_UI_Y), (x, ANGLE_UI_Y + PB_HEIGHT), LINE_THICKNESS)
    pygame.draw.line(WIN, GREY, (x, mp_y), (x + LINE_LEN, mp_y), LINE_THICKNESS)
    pygame.draw.line(WIN, RED, (x, mp_y), (x + angle_x, mp_y - angle_y), LINE_THICKNESS)
    pygame.draw.circle(WIN, BLACK, (x, mp_y), 5)

def draw_window(disc, goal, obstacle, parameters, graph_disc, time, ticks=0):
    WIN.fill(GREEN)
    WIN.blit(DISC, (disc.x, disc.y))

    timer = 0
    if time >= 0:
        timer = int(TIME_LIMIT / 1000 - int(time / 1000))

        #launch rotation
        cover_x = ROT_X + COVER_OFFSET + BAR_THICKNESS
        rotation_dir = "CW"
        rot_text_x = ROT_X + BAR_THICKNESS + BORDER
        if parameters.rotation == -1:
            rotation_dir = "CCW"
            rot_text_x = cover_x
            cover_x -= COVER_OFFSET
            
        rotation_text = ROTATION_FONT.render(rotation_dir, True, WHITE)
        rot_text_x = ROT_X + BAR_THICKNESS + (COVER_W - rotation_text.get_width())/2
        if parameters.rotation == -1:
            rot_text_x += COVER_OFFSET
        WIN.blit(rotation_text, (rot_text_x, ROT_TEXT_Y))
        cover = pygame.Rect(cover_x, COVER_Y, COVER_W, COVER_H)
        pygame.draw.rect(WIN, WHITE, ROT_BUTTON, BAR_THICKNESS)
        pygame.draw.rect(WIN, RED, cover, 0)
        
        #launch speed
        power_bar_fill = pygame.Rect(PB_X + BAR_THICKNESS, PB_Y + PIXELS_PER_MS*(27 - parameters.launch_speed), PB_WIDTH - 2*BAR_THICKNESS, parameters.launch_speed * PIXELS_PER_MS - 3)
        pygame.draw.rect(WIN, WHITE, POWER_BAR, BAR_THICKNESS)
        pygame.draw.rect(WIN, RED, power_bar_fill, 0)

        WIN.blit(POWER_TITLE, (POWER_TITLE_X, POWER_TITLE_Y))
        WIN.blit(ROT_TITLE, (ROT_TITLE_X, ROT_TITLE_Y))

        #draw goal and obstacle
        pygame.draw.rect(WIN, YELLOW, goal, 0)
        pygame.draw.rect(WIN, BROWN, obstacle, 0)

        #draw angles ui
        draw_angle_ui(VA_BL_X, parameters.launch_va, "Launch Angle")
        draw_angle_ui(HA_BL_X, parameters.launch_ha, "Launch Direction")
        draw_angle_ui(NA_BL_X, parameters.nose, "Nose Angle")
        draw_angle_ui(RA_BL_X, parameters.roll, "Roll Angle")

    else:
        timer = int(ticks/20)

        #graph
        graph_title = GRAPH_FONT.render("Elevation (y) vs Forward Distance (x)", True, WHITE)
        pygame.draw.rect(WIN, BLACK, goal, 0)
        pygame.draw.rect(WIN, BROWN, obstacle, 0)
        WIN.blit(graph_title, (GRAPH_TITLE_X, GRAPH_TITLE_Y))
        pygame.draw.rect(WIN, WHITE, Z_BAR, 1)
        pygame.draw.rect(WIN, WHITE, X_BAR, 1)
        pygame.draw.rect(WIN, RED, graph_disc, 0)

    timer_text = TIMER_FONT.render(str(timer), True, WHITE)
    WIN.blit(timer_text, (BORDER, BORDER))

    pygame.display.update()

def controls(keys_pressed, parameters):
    #e for ccw, r for cw
    #1,2 for power (0 - 27 in intervals of 0.25)
    #3,4 for launch angle (-90 - 90, intervals of 1)
    #5,6 for launch direction (-90 - 90, intervals of 1)
    #7,8 for nose (-90 - 90, intervals of 1)
    #9,0 for roll (-90 - 90, intervals of 1)
    if keys_pressed[pygame.K_e]:
        parameters.rotation = -1
    if keys_pressed[pygame.K_r]:
        parameters.rotation = 1
    if keys_pressed[pygame.K_1]:
        if parameters.launch_speed > 0:
            parameters.launch_speed -= POWER_SCALE
    if keys_pressed[pygame.K_2]:
        if parameters.launch_speed < 27:
            parameters.launch_speed += POWER_SCALE
    if keys_pressed[pygame.K_3]:
        if parameters.launch_va > -90:
            parameters.launch_va -= DEGREE_SCALE
    if keys_pressed[pygame.K_4]:
        if parameters.launch_va < 90:
            parameters.launch_va += DEGREE_SCALE
    if keys_pressed[pygame.K_5]:
        if parameters.launch_ha > -90:
            parameters.launch_ha -= DEGREE_SCALE
    if keys_pressed[pygame.K_6]:
        if parameters.launch_ha < 90:
            parameters.launch_ha += DEGREE_SCALE
    if keys_pressed[pygame.K_7]:
        if parameters.nose > -90:
            parameters.nose -= DEGREE_SCALE
    if keys_pressed[pygame.K_8]:
        if parameters.nose < 90:
            parameters.nose += DEGREE_SCALE
    if keys_pressed[pygame.K_9]:
        if parameters.roll > -90:
            parameters.roll -= DEGREE_SCALE
    if keys_pressed[pygame.K_0]:
        if parameters.roll < 90:
            parameters.roll += DEGREE_SCALE


# (lx, ly)----(ux, ly)
#    |             |
#    |             |
#    |             |
# (lx, uy)----(ux, uy)
def is_intersect(a_lx, a_ux, a_ly, a_uy, b_lx, b_ux, b_ly, b_uy):
    if b_ux > a_lx and b_uy > b_uy:
        return True
    if b_lx < a_lx and b_uy > a_ly:
        return True
    if b_ux > a_lx and b_ly < a_uy:
        return True
    if b_lx < a_ux and b_ly < a_uy:
        return True
    return False


def generate_obj():
    goal_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
    goal_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    obstacle_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
    obstacle_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    #while obstacle_x == goal_x:
    #    obstacle_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
    #while obstacle_y == goal_y:
    #    obstacle_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    while(is_intersect(goal_x, goal_x + OBJ_SIZE, goal_y, goal_y + OBJ_SIZE, obstacle_x, obstacle_x + OBJ_SIZE, obstacle_y, obstacle_y + OBJ_SIZE)):
        obstacle_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
        obstacle_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    goal = pygame.Rect(goal_x, goal_y, OBJ_SIZE, OBJ_SIZE)
    obstacle = pygame.Rect(obstacle_x, obstacle_y, OBJ_SIZE, OBJ_SIZE)
    return goal, obstacle

def main():
    start_y = random.randrange(START_Y_LOWER, START_Y_UPPER)
    goal, obstacle = generate_obj()
    disc = pygame.Rect(START_X, start_y, DISC_SIZE, DISC_SIZE)
    graph_disc = pygame.Rect(GRAPH_LOWER_X_BOUND, GRAPH_LOWER_Y_BOUND, 5, 5)
    pre_launch = True
    current_time = 0
    transition_time = 0
    disc_pos_index = 0
    position_array = None
    
    parameters = Parameters()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        current_time = pygame.time.get_ticks()
        if pre_launch and current_time >= TIME_LIMIT:
            position_array = throw_wrapper(parameters)
            pre_launch = False
            transition_time = current_time

        if pre_launch:
            draw_window(disc, goal, obstacle, parameters, graph_disc, current_time)
            keys_pressed = pygame.key.get_pressed()
            controls(keys_pressed, parameters)     
        else:
            launching_time = current_time - transition_time
            if launching_time > disc_pos_index * INTERVAL_LEN:
                disc_pos_index += 1
                current_position = position_array[disc_pos_index]
                if current_position[2] <= 0:
                    break
                disc.x = START_X + current_position[0]*FT_TO_PIXELS
                disc.y = start_y + current_position[1]*FT_TO_PIXELS
                graph_disc.x = GRAPH_LOWER_X_BOUND + current_position[0]
                graph_disc.y = GRAPH_LOWER_Y_BOUND - current_position[2]
            draw_window(disc, goal, obstacle, parameters, graph_disc, -1, disc_pos_index)

    pygame.quit()

if __name__ == "__main__":
    main()