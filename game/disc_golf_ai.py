import pygame
import random
from disc_flight import *
from parameters import *
from constants import *

def is_intersect(a_lx, a_ux, a_ly, a_uy, b_lx, b_ux, b_ly, b_uy):
    if a_lx < b_ux and b_ux < a_ux and a_ly < b_uy and b_uy < a_uy:
        return True
    if a_lx < b_ux and b_ux < a_ux and a_ly < b_ly and b_ly < a_uy:
        return True
    if a_lx < b_lx and b_lx < a_ux and a_ly < b_uy and b_uy < a_uy:
        return True
    if a_lx < b_lx and b_lx < a_ux and a_ly < b_ly and b_ly < a_uy:
        return True
    return False

def generate_obj():
    goal_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
    goal_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    obstacle_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
    obstacle_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    while(is_intersect(goal_x, goal_x + OBJ_SIZE, goal_y, goal_y + OBJ_SIZE, obstacle_x, obstacle_x + OBJ_SIZE, obstacle_y, obstacle_y + OBJ_SIZE)):
        obstacle_x = random.randrange(OBJ_LOWER_X, OBJ_UPPER_X)
        obstacle_y = random.randrange(OBJ_LOWER_Y, OBJ_UPPER_Y)
    goal = pygame.Rect(goal_x, goal_y, OBJ_SIZE, OBJ_SIZE)
    obstacle = pygame.Rect(obstacle_x, obstacle_y, OBJ_SIZE, OBJ_SIZE)
    return goal, obstacle

def get_distance(disc, goal):
    x_diff_sq = (disc[0] - goal[0])**2
    y_diff_sq = (disc[1] - goal[1])**2
    z_diff_sq = (disc[2] - goal[2])**2
    return np.sqrt(x_diff_sq + y_diff_sq + z_diff_sq)

class DiscGolfAI:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.start_y = random.randrange(START_Y_LOWER, START_Y_UPPER)
        self.goal, self.obstacle = generate_obj()
        self.disc = pygame.Rect(START_X, self.start_y, DISC_SIZE, DISC_SIZE)
        self.graph_disc = pygame.Rect(GRAPH_LOWER_X_BOUND, GRAPH_LOWER_Y_BOUND, 5, 5)
        self.pre_launch = True
        self.current_time = 0
        self.transition_time = 0
        self.disc_pos_index = 0
        self.position_array = None
        self.disc_z = LAUNCH_HEIGHT
        self.min_distance = np.inf
        self.parameters = Parameters()
    
    def draw_angle_ui(self, x, angle, title):
        mp_y = ANGLE_UI_Y + PB_HEIGHT/2
        angle_x = LINE_LEN * np.cos(np.radians(angle))
        angle_y = LINE_LEN * np.sin(np.radians(angle))

        text = ANGLE_FONT.render(title, True, WHITE)
        WIN.blit(text, (x + (LINE_LEN - text.get_width())/2, ANGLE_UI_Y - ANGLE_TITLE_Y_OFFSET))

        pygame.draw.line(WIN, BLACK, (x, ANGLE_UI_Y), (x, ANGLE_UI_Y + PB_HEIGHT), LINE_THICKNESS)
        pygame.draw.line(WIN, WHITE, (x, mp_y), (x + LINE_LEN, mp_y), LINE_THICKNESS)
        pygame.draw.line(WIN, RED, (x, mp_y), (x + angle_x, mp_y - angle_y), LINE_THICKNESS)
        pygame.draw.circle(WIN, BLACK, (x, mp_y), 5)

    def draw_window(self):
        WIN.fill(GREEN)
        WIN.blit(DISC, (self.disc.x, self.disc.y))
        timer = 0
        if self.pre_launch:
            timer = int(TIME_LIMIT / 1000 - int(self.current_time / 1000))

            #rotation control
            cover_x = ROT_X + COVER_OFFSET + BAR_THICKNESS
            rotation_dir = "CW"
            rot_text_x = ROT_X + BAR_THICKNESS + BORDER
            if self.parameters.rotation == -1:
                rotation_dir = "CCW"
                rot_text_x = cover_x
                cover_x -= COVER_OFFSET
            rotation_text = ROTATION_FONT.render(rotation_dir, True, WHITE)
            rot_text_x = ROT_X + BAR_THICKNESS + (COVER_W - rotation_text.get_width())/2
            if self.parameters.rotation == -1:
                rot_text_x += COVER_OFFSET
            WIN.blit(rotation_text, (rot_text_x, ROT_TEXT_Y))
            cover = pygame.Rect(cover_x, COVER_Y, COVER_W, COVER_H)
            pygame.draw.rect(WIN, WHITE, ROT_BUTTON, BAR_THICKNESS)
            pygame.draw.rect(WIN, RED, cover, 0)

            #launch speed
            power_bar_fill = pygame.Rect(PB_X + BAR_THICKNESS, PB_Y + PIXELS_PER_MS*(27 - self.parameters.launch_speed), PB_WIDTH - 2*BAR_THICKNESS, self.parameters.launch_speed * PIXELS_PER_MS - 3)
            pygame.draw.rect(WIN, WHITE, POWER_BAR, BAR_THICKNESS)
            pygame.draw.rect(WIN, RED, power_bar_fill, 0)

            WIN.blit(POWER_TITLE, (POWER_TITLE_X, POWER_TITLE_Y))
            WIN.blit(ROT_TITLE, (ROT_TITLE_X, ROT_TITLE_Y))

            #draw goal and obstacle
            pygame.draw.rect(WIN, GREY, self.goal, 0)
            pygame.draw.rect(WIN, BROWN, self.obstacle, 0)

            #draw angles ui
            self.draw_angle_ui(VA_BL_X, self.parameters.launch_va, "Launch Angle")
            self.draw_angle_ui(HA_BL_X, self.parameters.launch_ha, "Launch Direction")
            self.draw_angle_ui(NA_BL_X, self.parameters.nose, "Nose Angle")
            self.draw_angle_ui(RA_BL_X, self.parameters.roll, "Roll Angle")
        else:
            timer = int(self.disc_pos_index/20)

            #goal and obstacle
            pygame.draw.rect(WIN, GREY, self.goal, 0)
            pygame.draw.rect(WIN, BROWN, self.obstacle, 0)

            #graph
            #graph axes
            graph_title = GRAPH_FONT.render("Elevation (y) vs Forward Distance (x)", True, WHITE)
            
            WIN.blit(graph_title, (GRAPH_TITLE_X, GRAPH_TITLE_Y))
            pygame.draw.rect(WIN, WHITE, Z_BAR, 1)
            pygame.draw.rect(WIN, WHITE, X_BAR, 1)

            #graph objects
            graph_obs = pygame.Rect(GRAPH_LOWER_X_BOUND + self.obstacle.x/FT_TO_PIXELS, GRAPH_LOWER_Y_BOUND - OBSTACLE_Z, OBJ_SIZE/FT_TO_PIXELS, OBSTACLE_Z + 6)
            graph_goal = pygame.Rect(GRAPH_LOWER_X_BOUND + self.goal.x/FT_TO_PIXELS, GRAPH_LOWER_Y_BOUND - GOAL_UPPER_Z, OBJ_SIZE/FT_TO_PIXELS, GOAL_UPPER_Z - GOAL_LOWER_Z)
            graph_goal_post = pygame.Rect(GRAPH_LOWER_X_BOUND + self.goal.x/FT_TO_PIXELS + (OBJ_SIZE/FT_TO_PIXELS)/2 - 2, GRAPH_LOWER_Y_BOUND - GOAL_UPPER_Z, 2, GOAL_LOWER_Z * FT_TO_PIXELS)
            pygame.draw.rect(WIN, BROWN, graph_obs, 0)
            pygame.draw.rect(WIN, BLACK, graph_goal_post, 0)
            pygame.draw.rect(WIN, GREY, graph_goal, 0)
            pygame.draw.rect(WIN, RED, self.graph_disc, 0)

        timer_text = TIMER_FONT.render(str(timer), True, WHITE)
        WIN.blit(timer_text, (BORDER, BORDER))
        pygame.display.update()

    def input_control(self, keys_pressed):
        #e for ccw, r for cw
        #1,2 for power (0 - 27 in intervals of 0.25)
        #3,4 for launch angle (-90 - 90, intervals of 1)
        #5,6 for launch direction (-90 - 90, intervals of 1)
        #7,8 for nose (-90 - 90, intervals of 1)
        #9,0 for roll (-90 - 90, intervals of 1)
        if keys_pressed[pygame.K_e]:
            self.parameters.rotation = -1
        if keys_pressed[pygame.K_r]:
            self.parameters.rotation = 1
        if keys_pressed[pygame.K_1]:
            if self.parameters.launch_speed > 0:
                self.parameters.launch_speed -= POWER_SCALE
        if keys_pressed[pygame.K_2]:
            if self.parameters.launch_speed < 27:
                self.parameters.launch_speed += POWER_SCALE
        if keys_pressed[pygame.K_3]:
            if self.parameters.launch_va > -90:
                self.parameters.launch_va -= DEGREE_SCALE
        if keys_pressed[pygame.K_4]:
            if self.parameters.launch_va < 90:
                self.parameters.launch_va += DEGREE_SCALE
        if keys_pressed[pygame.K_5]:
            if self.parameters.launch_ha > -90:
                self.parameters.launch_ha -= DEGREE_SCALE
        if keys_pressed[pygame.K_6]:
            if self.parameters.launch_ha < 90:
                self.parameters.launch_ha += DEGREE_SCALE
        if keys_pressed[pygame.K_7]:
            if self.parameters.nose > -90:
                self.parameters.nose -= DEGREE_SCALE
        if keys_pressed[pygame.K_8]:
            if self.parameters.nose < 90:
                self.parameters.nose += DEGREE_SCALE
        if keys_pressed[pygame.K_9]:
            if self.parameters.roll > -90:
                self.parameters.roll -= DEGREE_SCALE
        if keys_pressed[pygame.K_0]:
            if self.parameters.roll < 90:
                self.parameters.roll += DEGREE_SCALE

    def adjust_for_launch_angle(self):
        theta = self.parameters.launch_ha * -1
        diff_x = self.disc.x - START_X
        diff_y = self.disc.y - self.start_y
        x = (diff_x * np.cos(np.radians(theta))) - (diff_y * np.sin(np.radians(theta)))
        y = (diff_y * np.cos(np.radians(theta))) + (diff_x * np.sin(np.radians(theta)))
        self.x = x + START_X
        self.y = y + self.start_y

    def game_over(self):
        return True, self.min_distance, self.current_time

    def play_step(self, time_adjust):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.current_time = int(pygame.time.get_ticks())
        self.current_time -= time_adjust
        if self.pre_launch and self.current_time >= TIME_LIMIT:
            self.position_array = throw_wrapper(self.parameters)
            self.pre_launch = False
            self.transition_time = self.current_time

        if self.pre_launch:
            self.draw_window()
            keys_pressed = pygame.key.get_pressed()
            self.input_control(keys_pressed)   
        else:
            launching_time = self.current_time - self.transition_time
            if launching_time > (self.disc_pos_index + 1) * INTERVAL_LEN:
                self.disc_pos_index += 1
                current_position = self.position_array[self.disc_pos_index]
                self.disc_z = current_position[2]
                #game over for disc touching ground
                if self.disc_z <= 0:
                    print("Landed")
                    return self.game_over()
                self.disc.x = START_X + current_position[0]*FT_TO_PIXELS
                self.disc.y = self.start_y + current_position[1]*FT_TO_PIXELS
                self.adjust_for_launch_angle()
                self.graph_disc.x = GRAPH_LOWER_X_BOUND + (self.disc.x - START_X)/FT_TO_PIXELS
                self.graph_disc.y = GRAPH_LOWER_Y_BOUND - self.disc_z
            disc_mp_xyz = [self.disc.x + DISC_SIZE/2, self.disc.y + DISC_SIZE/2, self.disc_z*FT_TO_PIXELS]
            goal_mp_xyz= [self.goal.x + OBJ_SIZE/2, self.goal.y + OBJ_SIZE/2, GOAL_MP_Z*FT_TO_PIXELS]
            self.min_distance = min(self.min_distance, get_distance(disc_mp_xyz, goal_mp_xyz))
            if is_intersect(self.goal.x, self.goal.x + OBJ_SIZE, self.goal.y, self.goal.y + OBJ_SIZE, self.disc.x, self.disc.x + DISC_SIZE, self.disc.y, self.disc.y + DISC_SIZE):
                if GOAL_LOWER_Z <= self.disc_z and self.disc_z <= GOAL_UPPER_Z:
                    print("Previous minimum distance from goal (ft): ", self.min_distance/FT_TO_PIXELS)
                    self.min_distance = 0
                    print("Goal")
                    return self.game_over()
                else:
                    print("Not within goal height: ", self.disc_z)
            if is_intersect(self.obstacle.x, self.obstacle.x + OBJ_SIZE, self.obstacle.y, self.obstacle.y + OBJ_SIZE, self.disc.x, self.disc.x + DISC_SIZE, self.disc.y, self.disc.y + DISC_SIZE):
                if self.disc_z <= OBSTACLE_Z:
                    print("Hit Obstacle")
                    return self.game_over()
        self.draw_window()
        return False, self.min_distance, 0

if __name__ == "__main__":
    game = DiscGolfAI()
    time_adjust = 0

    while True:
        game_over, min_distance, run_time = game.play_step(time_adjust)
        time_adjust += run_time
        if game_over:
            break
    
    print('Minimum Distance: ', min_distance)