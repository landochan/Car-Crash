import pygame
from Constants import *
import pyghelpers
from Play import *
from Splash import *
from Pick import *
from Highscore import *
from Level_Mgr import *
from Level import *
from Credits import *
from Introduction import *

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('CAR CRASH')
    icon = pygame.image.load('images/cars/cars_racer_red.png')
    pygame.display.set_icon(icon)

    oScenesList = [Introduction(window),
                   Splash(window),
                   Pick(window),
                   Play(window),
                   Level_Mgr(window),
                   Level(window),
                   Highscore(window),
                   Credits(window)]

    oSceneMgr = pyghelpers.SceneMgr(oScenesList, FPS)
    oSceneMgr.run()