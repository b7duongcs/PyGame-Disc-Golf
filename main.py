import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1500, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disc Golf")

GREEN = (0,128,0)
WHITE = (255, 255, 255)

FPS = 60
TICKS_PER_FRAME = 1000/FPS
TIME_LIMIT = 10000

FONT = pygame.font.Font('freesansbold.ttf', 32)

DISC_SIZE = 64
DISC_IMAGE = pygame.image.load(os.path.join('assets', 'disc_sprite.png'))
DISC = pygame.transform.scale(DISC_IMAGE, (DISC_SIZE, DISC_SIZE))


def draw_window(disc, colour, time):
    WIN.fill(colour)
    WIN.blit(DISC, (disc.x, disc.y))
    if time >= 0:
        timer = 10 - int(time / 1000)
        text = FONT.render(str(timer), True, WHITE)
        WIN.blit(text, (10,10))
    pygame.display.update()

def main():
    disc = pygame.Rect(4, 368, DISC_SIZE, DISC_SIZE)
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
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d]:
            disc.x += 1
        if not launching:
            draw_window(disc, GREEN, current_time)
        else:
            draw_window(disc, (0,0,0), -1)

    pygame.quit()

if __name__ == "__main__":
    main()