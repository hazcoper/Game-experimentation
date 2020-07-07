"""Used to create a base empty map, it will create the outside walls for the given resolution
and pixel size"""

resolution = 640, 480
pixel_size = 16
map_size = int(resolution[0]/pixel_size),int(resolution[1]/pixel_size)
print(map_size)
coords = []

def add_line(line,maze):
    for number in line:
        maze = maze + str(number)
    maze = maze + "\n"
    return maze

maze = ""
line = []

#First line
y = 2
for x in range(map_size[0]): #First line
    line.append(1)
    coords.append((x*16,y*16))
maze = add_line(line,maze)

while y < map_size[1]:
    coords.append((x*16, y*16))
    x = 2
    line = [1]
    while x < map_size[0]:
        line.append(0)
        x = x + 1
    line.append(1)
    y = y + 1
    maze = add_line(line,maze)

line = []                   #Last line
for x in range(map_size[0]):
        line.append(1)
        coords.append((x*16, y*16))
maze = add_line(line,maze)
print(coords)

#Write to file
file_name = "test.txt"
fileW = open(file_name, "w", encoding="UTF-8")
for e in maze:
    fileW.write(e)

fileW.close()