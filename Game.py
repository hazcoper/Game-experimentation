import pygame
import os
import time


"""New version of the game, basically copying the game that I donwloaded on my phone
Basically the player will move until it reaches a wall, and then it will stop

Thigns to do:
    Change the movement
        go until the wall
        add acceleration to the movement
    change the view mode
    make new maps"""

walls = [] #List of walls
# os.environ["SDL_VIDEO_CENTERED"] = "1" #Center the window
pygame.init()
screen = pygame.display.set_mode((640,480)) #setting the resolution
# screen = pygame.display.set_mode((320,240))
clock = pygame.time.Clock()

class Player():

    def __init__(self,pos,catch,points):
        self.rect = pygame.Rect(pos[0], pos[1],16,16)
        self.catch = catch
        self.points = points
        self.speed = 1

    def add_point(self, quant):
        self.points = self.points + 1

    def set_pos(self,pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def invert_catch(self):
        self.catch = not self.catch

    def move(self,dx, dy):
        #Movement is done one at a time
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx,dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: #Moving right, hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: #Moving left, hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: #Moving down, hit the top of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: #Moving up, hit the bottom of the wall
                    self.rect.top = wall.rect.bottom
    
    def new_move(self):
        "check if the next block""
class Wall():
    def __init__(self,pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16,16)

class Obj():
    def __init__(self,pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

def parse_map(file_name):
    """Gets a file containing a map, and parses it to a local representation"""
    with open(file_name, "r", encoding="UTF-8") as file:
        lines = file.readlines()
    maze = ""
    for e in lines:
        maze = maze + e
    return maze

def map_to_game(maze):
    """Turns the parsed mazed to walls and sets everythig in the right position"""
    y = 0
    x = 0
    for e in maze:
        if e == "1":
            Wall((x,y))
            x = x +16
        if e == "\n":
            y = y + 16
            x = 0
        if e == "0":
            x = x + 16
        if e == "A":
            p1_pos = (x,y)
            x = x + 16
        if e == "B":
            p2_pos = (x,y)
            x = x +16
        if e == "O":
            obj1 = (x,y)
            x = x + 16
    return p1_pos, p2_pos, obj1

def screen_update():
    screen.fill((0,0,0))
    for wall in walls:
        pygame.draw.rect(screen, (255,255,255), wall.rect)
    pygame.draw.rect(screen, (255, 58, 16), player1.rect)
    pygame.draw.rect(screen, (126,255,16), player2.rect)
    pygame.draw.rect(screen, (6, 255, 253) , obj1.rect)
    P1Score = font.render("Player 1: " + str(player1.points), 1, (0,0,255))
    P2Score = font.render("Player 2: " + str(player2.points), 1, (0,0,255))
    # screen.blit(P1Score, (180, -2))
    # screen.blit(P2Score, (380, -2))
    pygame.display.flip()

def round_end():
    player1.invert_catch()
    player2.invert_catch()
    player1.set_pos(p1_pos)
    player2.set_pos(p2_pos)


running = True
font = pygame.font.SysFont("helvetica", 16, True)
maze = parse_map("map.txt")
p1_pos, p2_pos, obj_pos = map_to_game(maze)
obj1 = Obj(obj_pos)
player1 = Player(p1_pos,True, 0)
player2 = Player(p2_pos, False, 0)
maze = parse_map("map.txt")



while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit without Errors
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Back to main screen
            exec(open("MainScreen.py").read())
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player1.move(-player1.speed,0)
    if key[pygame.K_d]:
        player1.move(player1.speed, 0)
    if key[pygame.K_w]:
        player1.move(0, -player1.speed)
    if key[pygame.K_s]:
        player1.move(0, player1.speed)
    if key[pygame.K_LEFT]:
        player2.move(-1, 0)
    if key[pygame.K_RIGHT]:
        player2.move(1, 0)
    if key[pygame.K_UP]:
        player2.move(0, -1)
    if key[pygame.K_DOWN]:
        player2.move(0, 1)

    #Check collision with obj
    if player1.rect.colliderect(obj1) and not player1.catch:
        player1.add_point(1)  #Player one has reached obj, invert role, reset map, and wait for user input
        print("Player 1 got the obj")
        round_end()
    if player2.rect.colliderect(obj1) and  not player2.catch:
        player2.add_point(1)
        print("Player 2 got the obj")
        round_end()
    if player1.rect.colliderect(player2):
        if player1.catch:
            player1.add_point(1)
            print("Player 1 caught 2")
            round_end()
        else:
            player2.add_point(1)
            print("Player 2 caught 1")
            round_end()
    screen_update()