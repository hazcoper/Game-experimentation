import pygame
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen_size = (640,480)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Tank game")


def screen_update():
    screen.fill((0,0,0))
    screen.blit(new_surf, (10,10))

    pygame.display.flip()

running = True
my_square = pygame.Rect(30, 30, 16,16)




x = 0
while running:
    x = x + 0.01
    clock.tick(120)

    surf = pygame.Surface((my_square.w, my_square.h))
    surf.fill((255, 255, 0))
    new_surf = pygame.transform.rotate(surf,120)
    print(surf)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen_update()