import pygame
import os


""""Menu and main screen for the Catch V2 Game"""

# os.environ["SDL_VIDEO_CENTERED"] = "1" #Center the window
pygame.init()
screen_size = (640,480)
screen = pygame.display.set_mode(screen_size) #setting the resolution
clock = pygame.time.Clock()
pygame.display.set_caption("CatchGameV2")

images = {1: "Play.jpg", 2: "LevelMaker.jpg", 3: "Settings.jpg", 4: "EXIT.jpg"}
font = pygame.font.SysFont("helvetica", 23, True)
current = pygame.image.load("menu/"+ images[1])


def draw_text():
    Tutorial_cap = font.render("T for TUTORIAL", 1, (229, 242, 51))
    Tutorial_cap_size = pygame.Surface.get_size(Tutorial_cap)
    Credits_cap = font.render("C for CREDITS", 1, (229, 242, 51))
    Credits_cap_size = pygame.Surface.get_size(Credits_cap)

    screen.blit(Credits_cap, (7,screen_size[1]-7-Credits_cap_size[1]))
    screen.blit(Tutorial_cap, (screen_size[0]-7-Tutorial_cap_size[0],screen_size[1]-7-Tutorial_cap_size[1]))

def screen_update():

    screen.fill((0,0,0))
    screen.blit(current, (0,0))
    draw_text()

    pygame.display.flip()


running = True
image_counter = 1

while running:
    clock.tick(120)

    current = pygame.image.load("menu/" + images[image_counter])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Back to main screen
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                exec(open("Credits.py").read())
                running = False
            if event.key  == pygame.K_w:
                if image_counter > 1:
                    image_counter -= 1
                else:
                    image_counter = len(images)
            if event.key == pygame.K_s:
                if image_counter < len(images):
                    image_counter += 1
                else:
                    image_counter = 1
            if event.key == pygame.K_RETURN:
                if image_counter == 1: # Play the game
                    exec(open("Game.py").read())
                    image_counter == 1
                    running = False
                if image_counter == 2: # Create Map
                    exec(open("MapMaker.py").read())
                    image_counter == 2
                    running = False
                if image_counter == 3: # Settings
                    exec(open("Settings.py").read())
                    image_counter == 3
                    pass
                if image_counter == 4: #Exit
                    running = False

    screen_update()