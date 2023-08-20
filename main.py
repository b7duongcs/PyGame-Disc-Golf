import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disc Golf")

GREEN = (0,128,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
TICKS_PER_FRAME = 1000/FPS
TIME_LIMIT = 10000

FONT = pygame.font.Font('freesansbold.ttf', 32)

DISC_SIZE = 32
DISC_IMAGE = pygame.image.load(os.path.join('assets', 'disc_sprite.png'))
DISC = pygame.transform.scale(DISC_IMAGE, (DISC_SIZE, DISC_SIZE))

START_X = 10
START_Y = (HEIGHT - DISC_SIZE) / 2

def draw_window(disc, colour, time):
    WIN.fill(colour)
    WIN.blit(DISC, (disc.x, disc.y))
    if time >= 0:
        timer = int(TIME_LIMIT / 1000 - int(time / 1000))
        text = FONT.render(str(timer), True, WHITE)
        WIN.blit(text, (10,10))
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
    launching = False #false: inputting controls, true: watching disc fly, no inputs
    current_time = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        current_time = pygame.time.get_ticks()
        if current_time >= TIME_LIMIT:
            launching = True

        if not launching:
            draw_window(disc, GREEN, current_time)
            keys_pressed = pygame.key.get_pressed()
            controls(keys_pressed, disc)
        else:
            draw_window(disc, BLACK, -1)

    pygame.quit()

if __name__ == "__main__":
    main()