# Background consists of grass, trees and roads
import pygame, random
import pygwidgets
from Constants import *

import sys
from pygame.locals import *

# This class creates one Background the size of the display
class Background():
    GRASS_IMG = pygame.image.load('images/grass/grass_enlarged2.png')
    ROAD_IMG = pygame.image.load('images/road/road_modified3.png')

    def __init__(self, window, numOfTrees, alpha):
        self.window = window
        self.tempSurface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        self.tempSurface = self.tempSurface.convert_alpha()
        self.tempSurface.blit(Background.GRASS_IMG, (0, 0))
        self.loc = (0, 0)
        treeImageList = []
        for i in range(numOfTrees):
            treeImage = pygame.image.load('images/trees/tree_%s.png'
                                           %(random.randint(1, 47)))
            instanceWidth = treeImage.get_width()
            instanceHeight = treeImage.get_height()
            colliding = True
            while colliding:
                locY = random.randint(0, WINDOWHEIGHT - instanceHeight)
                locX = random.randint(0, WINDOWWIDTH - instanceWidth)
                while (LEFTMARGIN - instanceWidth) <= locX <= RIGHTMARGIN:
                    locX = random.randint(0, WINDOWWIDTH - instanceWidth)
                instanceRect = pygame.Rect(locX, locY, instanceWidth, instanceHeight)
                colliding = False
                for treeImageItem in treeImageList:
                    if instanceRect.colliderect(treeImageItem.getRect()):
                        colliding = True
                        break

            treeImage = pygwidgets.Image(self.tempSurface, (locX, locY), treeImage)
            treeImageList.append(treeImage)

        for treeImage in treeImageList:
            treeImage.draw()

        self.tempSurface.set_alpha(alpha)

    def draw(self):
        self.window.blit(self.tempSurface, self.loc)
        self.window.blit(Background.ROAD_IMG, (self.loc[0] + LEFTMARGIN, self.loc[1]))

    def setLoc(self, loc):
        self.loc = loc

    def setTop(self, newTop):
        left, top = self.getLoc()
        self.setLoc((left, newTop))

    def setBottom(self, newBottom):
        newTop = newBottom - WINDOWHEIGHT
        self.setTop(newTop)

    def getLoc(self):
        return self.loc

    def getTop(self):
        return self.loc[1]

    def getBottom(self):
        top = self.getLoc()[1]
        return top + WINDOWHEIGHT



class BackgroundMgr():
    def __init__(self, window, cameraSpeed, alpha):
        self.window = window
        self.alpha = alpha
        self.cameraSpeed = cameraSpeed
        self.hidden = False
        self.startY = 0
        self.backgroundList = []
        oBackground = Background(self.window, NUM_OF_TREES, self.alpha)
        self.backgroundList.append(oBackground)
        self.update()

    def update(self):
        for oBackground in self.backgroundList:
            oldTop = oBackground.getTop()
            newTop = oldTop + self.cameraSpeed
            oBackground.setTop(newTop)
        self.startY += self.cameraSpeed

        # Add new background when the last background bottom pass y = 0
        if self.backgroundList[-1].getBottom() > 0:
            oBackground = Background(self.window, NUM_OF_TREES, self.alpha)
            oBackground.setBottom(self.backgroundList[-1].getTop())
            self.backgroundList.append(oBackground)

        if self.backgroundList[0].getTop() < WINDOWHEIGHT:
            oBackground = Background(self.window, NUM_OF_TREES, self.alpha)
            oBackground.setTop(self.backgroundList[0].getBottom())
            self.backgroundList.insert(0, oBackground)

        # Remove old background with top passing the bottom line
        if self.backgroundList[1].getTop() > WINDOWHEIGHT:
            del self.backgroundList[0]

    def getDistance(self):
        return self.startY

    def draw(self):
        if self.hidden:
            return

        for oBackground in self.backgroundList:
            oBackground.draw()

    def setCameraSpeed(self, newCameraSpeed):
        self.cameraSpeed = newCameraSpeed

    # for debug
    def getBackgroundListLength(self):
        return len(self.backgroundList)

    def getAllTop(self):
        topList = []
        for oBackground in self.backgroundList:
            topList.append(oBackground.getTop())
        return topList

    def hide(self):
        self.hidden = True

    def reset(self):
        self.startY = 0


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FPSCLOCK = pygame.time.Clock()

    cameraSpeed = 10
    oBackgroundMgr = BackgroundMgr(window, cameraSpeed)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        oBackgroundMgr.setCameraSpeed(cameraSpeed)
        oBackgroundMgr.update()

        window.fill('black')
        oBackgroundMgr.draw()
        pygame.display.update()
        FPSCLOCK.tick(30)

        # for debug
        print(oBackgroundMgr.getBackgroundListLength(), cameraSpeed, oBackgroundMgr.getAllTop())
