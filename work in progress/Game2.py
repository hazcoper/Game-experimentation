import pygame
from network import Network
import os
import time

"""Catch game version 2. Has a map editor (still work in progress), more flowy and better collision detection
Still need to finish map editor(someway to make maps)
add tittle screen, add boost, add timers, figure out the score system
maybe add multiplayer ability"""

walls = [] #List of walls
os.environ["SDL_VIDEO_CENTERED"] = "1" #Center the window
pygame.init()
screen = pygame.display.set_mode((640,480)) #setting the resolution
# screen = pygame.display.set_mode((320,240))
clock = pygame.time.Clock()

#Connect to the sever
# ip_add = input("What is the ip: ")
ip_add = "192.168.1.5"
while not ("net" in globals()):
    try:
        net = Network(ip_add)
    except:
        print("Trying again...")
        time.sleep(0.5)
print("Connection Sucessfull")
print(net.id)

class Player():

    def __init__(self,pos,catch,points):
        self.rect = pygame.Rect(pos[0], pos[1],16,16)
        self.catch = catch
        self.points = points
        self.speed = 1
        self.orginal_pos = pos
        self.x = self.rect.x
        self.y = self.rect.y

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
            self.x = self.rect.x
            self.y = self.rect.y
        if dy != 0:
            self.move_single_axis(0, dy)
            self.x = self.rect.x
            self.y = self.rect.y

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
    pygame.draw.rect(screen, (255, 58, 16), local.rect)
    pygame.draw.rect(screen, (126,255,16), online_player.rect)
    pygame.draw.rect(screen, (6, 255, 253) , obj1.rect)
    P1Score = font.render("Player 1: " + str(local.points), 1, (0,0,255))
    P2Score = font.render("Player 2: " + str(online_player.points), 1, (0,0,255))
    screen.blit(P1Score, (180, -2))
    screen.blit(P2Score, (380, -2))
    pygame.display.flip()

def round_end():
    local.invert_catch()
    online_player.invert_catch()
    local.set_pos(local.orginal_pos)
    print(online_player.orginal_pos)
    online_player.set_pos(online_player.orginal_pos)
    parse_data(send_data())

def send_data():
    data = str(net.id) + ":" + str(local.x) + "," + str(local.y)
    reply = net.send(data)
    return reply

def parse_data(data):
    try:
        d = data.split(":")[1].split(",")
        return int(d[0]), int(d[1])
    except:
        return 0,0


running = True
font = pygame.font.SysFont("helvetica", 16, True)
maze = parse_map("map.txt")
p1_pos, p2_pos, obj_pos = map_to_game(maze)
obj1 = Obj(obj_pos)

if net.id == "0":
    print("You are player one")
    local = Player(p1_pos,True, 0)
    online_player = Player(p2_pos, False, 0)
if net.id == "1":
    print("You are player 2")
    local = Player(p2_pos, False, 0)
    online_player = Player(p1_pos, True, 0)


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
        local.move(-1,0)
    if key[pygame.K_d]:
        local.move(1, 0)
    if key[pygame.K_w]:
        local.move(0,-1)
    if key[pygame.K_s]:
        local.move(0, 1)

    #Check collision with obj
    if local.rect.colliderect(obj1) and not local.catch:
        local.add_point(1)  #Player one has reached obj, invert role, reset map, and wait for user input
        print("Player 1 got the obj")
        round_end()
    if online_player.rect.colliderect(obj1) and  not online_player.catch:
        online_player.add_point(1)
        print("Player 2 got the obj")
        round_end()
    if local.rect.colliderect(online_player):
        if local.catch:
            local.add_point(1)
            print("Player 1 caught 2")
            round_end()
        else:
            online_player.add_point(1)
            print("Player 2 caught 1")
            round_end()

    p2x, p2y = parse_data(send_data())
    online_player.set_pos((p2x,p2y))
    screen_update()
