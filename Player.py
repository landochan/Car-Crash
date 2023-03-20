import pygwidgets
from Constants import *
from Car import *
from pygame.locals import *

class Player():
    def __init__(self, window, startLoc, playerSpeedX):
        self.window = window
        self.startLoc = startLoc
        self.playerSpeedX = playerSpeedX
        self.oCar = Car(self.window, self.startLoc, (0, 0), CAR_RED,
                        0)


    def draw(self):
        self.oCar.draw()
        self.oCar.drawFlame()

    def reset(self):
        self.oCar.setLoc(self.startLoc)
        self.oCar.setNotAflame()

    def handleEvents(self, keyPressed):
        speedX = 0
        loc = self.oCar.getLoc()

        if keyPressed[K_LEFT] or keyPressed[K_a]:
            speedX -= self.playerSpeedX
        if keyPressed[K_RIGHT] or keyPressed[K_d]:
            speedX += self.playerSpeedX

        newX = loc[0] + speedX
        if newX < LEFTMARGIN or newX > RIGHTMARGIN - CAR_WIDTH:
            speedX = 0

        self.oCar.setSpeed((speedX, 0))

    def update(self):
        self.oCar.update()

    def updateFlame(self):
        self.oCar.updateFlame()

    def getCar(self):
        return self.oCar

    def getAflame(self):
        return self.oCar.getAflame()

    def replace(self, carName):
        self.oCar.replace(carName)

    def setLoc(self, loc):
        self.oCar.setLoc(loc)
