import pygame, sys
import pygwidgets
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((600, 600))
oFireAnimation = pygwidgets.SpriteSheetAnimation(window, (0, 0), 'images/fire/sFire_strip3_enlarged.png',
                                                 3, 55, 55, 0.5, autoStart=True, loop=True)
FPSCLOCK = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    oFireAnimation.update()

    window.fill('black')
    oFireAnimation.draw()
    pygame.display.update()
    FPSCLOCK.tick(30)

