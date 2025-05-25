import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

garfieldImg = pygame.image.load('garfield.png') # 50x70
garfieldx = 350
garfieldy = 230
directionGarfield = 'up'

while True: # the main game loop
    DISPLAYSURF.fill(WHITE)

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    if directionGarfield == 'right':
        garfieldx += 5
        if garfieldx == 350:
            directionGarfield = 'up'
    elif directionGarfield == 'down':
        garfieldy += 5
        if garfieldy == 230:
            directionGarfield = 'right'
    elif directionGarfield == 'left':
        garfieldx -= 5
        if garfieldx == 0:
            directionGarfield = 'down'
    elif directionGarfield == 'up':
        garfieldy -= 5
        if garfieldy == 0:
            directionGarfield = 'left'


    DISPLAYSURF.blit(catImg, (catx, caty))
    DISPLAYSURF.blit(garfieldImg,(garfieldx,garfieldy))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)