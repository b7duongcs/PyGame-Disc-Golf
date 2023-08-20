import pygame
import os
from disc_flight import *

pygame.init()

WIDTH, HEIGHT = 1500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disc Golf")

GREEN = (0,128,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
TICKS_PER_FRAME = 1000/FPS
TIME_LIMIT = 2000

FONT = pygame.font.Font('freesansbold.ttf', 32)

DISC_SIZE = 32
DISC_IMAGE = pygame.image.load(os.path.join('assets', 'disc_sprite.png'))
DISC = pygame.transform.scale(DISC_IMAGE, (DISC_SIZE, DISC_SIZE))

START_X = 10
START_Y = (HEIGHT - DISC_SIZE) / 2

def draw_window(disc, colour, time, ticks=0):
    WIN.fill(colour)
    WIN.blit(DISC, (disc.x, disc.y))
    timer = 0
    if time >= 0:
        timer = int(TIME_LIMIT / 1000 - int(time / 1000))
    else:
        timer = int(ticks/20)
    timer_text = FONT.render(str(timer), True, WHITE)
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
            position_array = get_position_array()
            pre_launch = False

        if pre_launch:
            draw_window(disc, GREEN, current_time)
            keys_pressed = pygame.key.get_pressed()
            controls(keys_pressed, disc)
            transition_time = current_time
        else:
            #calculate (x,y,z) at each 50ms interval with external function
            #return list of (x,y,z)
            #draw (x,y,z)
            launching_time = current_time - transition_time
            if launching_time > disc_pos_index * 50:
                disc_pos_index += 1
                current_position = position_array[disc_pos_index]
                if current_position[2] <= 0:
                    print("z position is ", current_position[2])
                    break
                disc.x += position_array[disc_pos_index][0]
                disc.y += position_array[disc_pos_index][1]
            draw_window(disc, BLACK, -1, disc_pos_index)

    pygame.quit()

if __name__ == "__main__":
    main()