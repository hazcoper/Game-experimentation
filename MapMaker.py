import pygame
import os

"""Map creator for the catch game v2, still work in progress
Got player and player can add walls. And when map is rendered it saves the map
need to add the ability to check if map is valid"""

square_size = 16
walls_coord = []
wall_list = []
background = pygame.image.load("BackGround.png")
grid_toggle = True

#Making outer walls
outer_coords = []
for x in range(0,632, 16):
    outer_coords.append((x, 0))
    outer_coords.append((x, 480-16))
for y in range(0,480, 16):
    outer_coords.append((0,y))
    outer_coords.append((624,y))
outer_walls = [pygame.Rect(pos[0],pos[1],square_size,square_size) for pos in outer_coords]


pygame.init()
resolution = (640,480)
screen = pygame.display.set_mode(resolution)

clock = pygame.time.Clock()

class Player():

    def __init__(self, square_size):
        self.rect = pygame.Rect(16,16,16,16)
        self.color = (0,0,255)

    def move(self,dx, dy):
        #Movement is done one at a time
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx,dy):

        self.rect.x += dx
        self.rect.y += dy

        for wall in outer_walls:
            if self.rect.colliderect(wall):
                if dx > 0: #Moving right, hit the left side of the wall
                    self.rect.right = wall.left
                if dx < 0: #Moving left, hit the right side of the wall
                    self.rect.left = wall.right
                if dy > 0: #Moving down, hit the top of the wall
                    self.rect.bottom = wall.top
                if dy < 0: #Moving up, hit the bottom of the wall
                    self.rect.top = wall.bottom

def map_update(player_flag, grid_flag):
    screen.fill((0,0,0))
    if grid_flag:
        screen.blit(background, (0,0))

    for wall in outer_walls:
        pygame.draw.rect(screen, (255,255,255),wall)
    for wall in wall_list:
        pygame.draw.rect(screen, (255,255,255), wall)
    #draw player
    if player_flag:
        pygame.draw.rect(screen, player.color, player.rect)
    if "p1_spawn" in globals():
        rect = pygame.Rect(p1_spawn[0],p1_spawn[1],16,16)
        pygame.draw.rect(screen, (255,0,0), rect)
    if "p2_spawn" in globals():
        rect = pygame.Rect(p2_spawn[0],p2_spawn[1],16,16)
        pygame.draw.rect(screen, (0,255,0), rect)
    if "obj" in globals():
        rect = pygame.Rect(obj[0],obj[1],16,16)
        pygame.draw.rect(screen, (0,255,255), rect)
    pygame.display.flip()

def make_walls():
    for pos in walls_coord:
        wall = pygame.Rect(pos[0],pos[1],16,16)
        if wall not in wall_list:
            wall_list.append(pygame.Rect(pos[0],pos[1],16,16))

def make_map():
    if not ("p1_spawn" in globals() and "p2_spawn" in globals() and "obj" in globals()):
        print("Map is not valid")
        return
    x,y = 0,0
    maze = ""
    map_size = int(resolution[0] / square_size), int(resolution[1] / square_size)
    while y < resolution[1]:
        while x < resolution[0]:
            pos = (x,y)
            if pos in walls_coord or pos in outer_coords:
                maze = maze + "1"
            elif pos == p1_spawn:
                    maze = maze + "A"
            elif pos == p2_spawn:
                maze = maze + "B"
            elif pos == obj:
                maze = maze + "O"
            else:
                maze = maze + "0"
            x = x + 16
        maze = maze + "\n"
        x = 0
        y = y + 16

    # Write to file
    file_name = (input("Name of the file? ")).lower()

    #Check if the map already exist
    MapList = os.listdir("maps")

    if file_name in MapList:
        print("That map already exist, choose a new name and try again")
        return
    os.mkdir(os.path.join("maps", file_name))

    fileW = open(os.path.join("maps",file_name, file_name + ".txt"), "w", encoding="UTF-8")
    for e in maze:
        fileW.write(e)
    fileW.close()

    map_update(False,False)
    pygame.image.save(screen, os.path.join("maps",file_name, file_name + ".png"))

    print("Map has been saved")


player = Player(square_size)
running = True

while running:
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit without errors
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Back to main screen
            running = False
        if event.type == pygame.KEYDOWN  and event.key == pygame.K_g:
            grid_toggle = not grid_toggle

    # #Player movement
    key = pygame.key.get_pressed()

    if key[pygame.K_a]:
        player.move(-16, 0)
    if key[pygame.K_d]:
        player.move(16, 0)
    if key[pygame.K_w]:
        player.move(0, -16)
    if key[pygame.K_s]:
        player.move(0, 16)

    #Player actions
    if key[pygame.K_p]: #place a wall
        pos = (player.rect.x, player.rect.y)
        if pos not in walls_coord:
            walls_coord.append(pos)

    if key[pygame.K_1]: #Player one spawn
        pos = player.rect.x, player.rect.y
        if pos not in walls_coord:
            p1_spawn = (player.rect.x, player.rect.y)

    if key[pygame.K_2]: #Player two spawn
        pos = player.rect.x, player.rect.y
        if pos not in walls_coord:
            p2_spawn = (player.rect.x, player.rect.y)

    if key[pygame.K_o]: #Obj
        pos = player.rect.x, player.rect.y
        if pos not in walls_coord:
            obj = (player.rect.x, player.rect.y)

    if key[pygame.K_SPACE]:
        pos = (player.rect.x, player.rect.y)
        if pos in walls_coord:
            walls_coord.remove(pos)
            for wall in wall_list:
                if player.rect.x == wall.x and player.rect.y == wall.y:
                    wall_list.remove(wall)

    if key[pygame.K_m]: #Make the map
        make_map()

    make_walls()
    map_update(True,grid_toggle)

exec(open("MainScreen.py").read())