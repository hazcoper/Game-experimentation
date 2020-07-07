import os
from shutil import copyfile
import pygame

"""Used to select the map the user wants to play, still work in progress"""


# os.environ["SDL_VIDEO_CENTERED"] = "1" #Center the window
pygame.init()
resolution = (640,480)
screen = pygame.display.set_mode(resolution) #setting the resolution
clock = pygame.time.Clock()
pygame.display.set_caption("CatchGameV2")
font = pygame.font.SysFont("helvetica", 30, True)

def display_name():
    name = MapList[x]
    textSurface = font.render(name, True, (255,255,255))
    textRect = textSurface.get_rect()
    textRect.center = ((resolution[0]/2), (resolution[1] /2)+200)
    screen.blit(textSurface,textRect)


def screen_update(image):
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,255,255), border)
    screen.blit(my_image,((640-512)/2, (450-384)/2))
    display_name()

    pygame.display.flip()



def map_list():
    MapList = os.listdir("maps")
    return MapList

running = True
MapList = map_list()
x = 0

file_name = MapList[0]
my_image = pygame.image.load(os.path.join("maps", file_name, file_name + ".png"))
my_image = pygame.transform.scale(my_image, (512, 384))
border = pygame.Rect((640-516)/2,(450-387)/2,516,387)

def change_image(value, x):
    x = x + (1*value)
    if x >= len(MapList):
        x = 0
    if x < 0:
        x = len(MapList) - 1
    file_name = MapList[x]
    my_image = pygame.image.load(os.path.join("maps", file_name, file_name + ".png"))
    my_image = pygame.transform.scale(my_image, (512, 384))
    return my_image, x


while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit without errors
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Back to main screen

            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            my_image, x = change_image(1,x)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            my_image, x = change_image(-1,x)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            """This means the player choose the current map
            Replace the map on the main directory and go back to main screen"""
            main_dir = os.getcwd() #"cache" current dir
            os.remove("map.txt") #Take the map out of the directory
            name = MapList[x]
            copyfile(os.path.join("maps", name, name + ".txt"),os.path.join(main_dir, "map.txt"))
            running = False


    screen_update(my_image)

exec(open("MainScreen.py").read())