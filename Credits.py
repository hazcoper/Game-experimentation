import pygame
import os

# os.environ["SDL_VIDEO_CENTERED"] = "1" # Center the window
pygame.init()
screen_size = (640,480)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.SysFont("helvetica", 23, True)


class Text():
    def __init__(self, text, color, y):
        self.text = text
        self.color = color
        self.surf = font.render(self.text, 1, color)
        self.size = pygame.Surface.get_size(self.surf)
        self.pos = [(screen_size[0]-self.size[0])/2, y]

    def scroll(self):
        if self.pos[1] > screen_size[1]:
            self.pos[1] = 0
        self.pos[1] = self.pos[1] + 0.35


def screen_update():
    screen.fill((0,0,0))
    for text in text_class_list:
        screen.blit(text.surf, text.pos)
        text.scroll()
    pygame.display.flip()

text_list = [
    "Hazcoper",
    "Made by:",
    "",
    "",
    "Hazcoper",
    "Graphics by:",
    "",
    "lol, cant you see there is no sound?",
    "Sounds by:",
    
]

text_class_list = []

for e in range(len(text_list)-1,-1,-1):
    print(text_list[e])
    if not text_list[e] == "":
        text_class_list.append(Text(text_list[e],(230, 230, 237),e*-25))
running = True

while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit without Errors
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Back to main screen
            exec(open("MainScreen.py").read())
            running = False
    screen_update()