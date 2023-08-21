import pygame
import os
from disc_flight import *

pygame.init()

WIDTH, HEIGHT = 1000, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disc Golf")

GRAPH_UPPER_Y_BOUND = HEIGHT - 65
GRAPH_LOWER_Y_BOUND = HEIGHT - 15
GRAPH_LOWER_X_BOUND = WIDTH - 215
Z_BAR = pygame.Rect(GRAPH_LOWER_X_BOUND - 2, GRAPH_UPPER_Y_BOUND + 5, 2, 50)
X_BAR = pygame.Rect(GRAPH_LOWER_X_BOUND - 2, GRAPH_LOWER_Y_BOUND + 5, 200, 2)
GRAPH_TITLE_X = GRAPH_LOWER_X_BOUND
GRAPH_TITLE_Y = GRAPH_UPPER_Y_BOUND - 20

GREEN = (0,128,0)
RED = (255,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
TICKS_PER_FRAME = 1000/FPS
TIME_LIMIT = 2000

TIMER_FONT = pygame.font.Font('freesansbold.ttf', 32)
GRAPH_FONT = pygame.font.Font('freesansbold.ttf', 10)

DISC_SIZE = 32
DISC_IMAGE = pygame.image.load(os.path.join('assets', 'disc_sprite.png'))
DISC = pygame.transform.scale(DISC_IMAGE, (DISC_SIZE, DISC_SIZE))

START_X = 10
START_Y = (HEIGHT - DISC_SIZE) / 2

def draw_window(disc, graph_disc, colour, time, ticks=0):
    WIN.fill(colour)
    WIN.blit(DISC, (disc.x, disc.y))
    timer = 0
    if time >= 0:
        timer = int(TIME_LIMIT / 1000 - int(time / 1000))
    else:
        timer = int(ticks/20)
        graph_title = GRAPH_FONT.render("Elevation (y) vs Forward Distance (x)", True, WHITE)
        WIN.blit(graph_title, (GRAPH_TITLE_X, GRAPH_TITLE_Y))
        pygame.draw.rect(WIN, WHITE, Z_BAR, 1)
        pygame.draw.rect(WIN, WHITE, X_BAR, 1)
        pygame.draw.rect(WIN, RED, graph_disc, 0)
    timer_text = TIMER_FONT.render(str(timer), True, WHITE)
    WIN.blit(timer_text, (10,10))
    pygame.display.update()

def controls(keys_pressed, disc):
    if keys_pressed[pygame.K_w]:
        disc.y -= 1
    if keys_pressed[pygame.K_a]:
        disc.x -= 1
    if keys_pressed[pygame.K_s]:
        disc.y += 1
    if keys_pressed[pygame.K_d]:
        disc.x += 1

def main():
    disc = pygame.Rect(START_X, START_Y, DISC_SIZE, DISC_SIZE)
    graph_disc = pygame.Rect(GRAPH_LOWER_X_BOUND, GRAPH_LOWER_Y_BOUND, 5, 5)
    pre_launch = True
    current_time = 0
    transition_time = 0
    disc_pos_index = 0
    position_array = None

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        current_time = pygame.time.get_ticks()
        if pre_launch and current_time >= TIME_LIMIT:
            position_array = throw("CW", 22.35, 10, 0, 0, 12)
            pre_launch = False
            transition_time = current_time

        if pre_launch:
            draw_window(disc, graph_disc, GREEN, current_time)
            keys_pressed = pygame.key.get_pressed()
            controls(keys_pressed, disc)     
        else:
            launching_time = current_time - transition_time
            if launching_time > disc_pos_index * 50:
                disc_pos_index += 1
                current_position = position_array[disc_pos_index]
                if current_position[2] <= 0:
                    break
                disc.x = START_X + current_position[0]*5
                disc.y = START_Y + current_position[1]*5
                graph_disc.x = GRAPH_LOWER_X_BOUND + current_position[0]/4
                graph_disc.y = GRAPH_LOWER_Y_BOUND - current_position[2]
            draw_window(disc, graph_disc, BLACK, -1, disc_pos_index)

    pygame.quit()

if __name__ == "__main__":
    main()