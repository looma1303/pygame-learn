import pygame, sys
from pygame.locals import *


pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World!')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0,0,128)


font0bj = pygame.font.Font('freesandsbold.ttf', 32)
textSurface0bj = font0bj.render('Hello world!', True, GREEND, BLUE)
textRect0bj = textSurface0bj.get_rect()
textRect0bj.center = (200, 150)

while True:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurface0bj, textRect0bj)
    for event in pygame.event.get():
        if event.type == QUIT():
            pygame.quit()
            sys.exit()
        pygame.display.update()
