import random
import pygame
import pygwidgets
from Constants import *

class Car():
    CAR_DICT = {CAR_RED: pygame.image.load('images/cars/cars_racer_red.png'),
                CAR_BLUE: pygame.image.load('images/cars/cars_racer_blue.png'),
                CAR_GREEN: pygame.image.load('images/cars/cars_racer_green.png'),
                CAR_YELLOW: pygame.image.load('images/cars/cars_racer_yellow.png')}

    def __init__(self, window, startLoc, speed, carChoice, cameraSpeed, direction='front'):
        self.window = window
        self.speed = speed
        self.cameraSpeed = cameraSpeed
        self.oImageCollection = pygwidgets.ImageCollection(self.window, startLoc, Car.CAR_DICT, carChoice)
        if direction == 'back':
            self.oImageCollection.rotate(180)
        self.aflame = False

    def draw(self):
        self.oImageCollection.draw()

    def drawFlame(self):
        if self.aflame:
            self.oFireAnimation.draw()


    def setLoc(self, newLoc):
        self.oImageCollection.setLoc(newLoc)
        if self.aflame:
            self.oFireAnimation.setLoc(newLoc)

    def getLoc(self):
        return self.oImageCollection.getLoc()

    def setSpeed(self, newSpeed):
        if self.aflame:
            return
        self.speed = newSpeed

    def update(self):
        loc = self.getLoc()
        self.setLoc((loc[0] + self.speed[0], loc[1] + self.speed[1] + self.cameraSpeed))

    def updateFlame(self):
        if self.aflame:
            self.oFireAnimation.update()

    def collideCar(self, otherCar):
        return self.oImageCollection.overlaps(otherCar.getRect())

    def getRect(self):
        return self.oImageCollection.getRect()

    def getSpeed(self):
        return self.speed

    def getAflame(self):
        return self.aflame

    def setAflame(self):
        if self.aflame:
            return
        self.aflame = True
        self.oFireAnimation = pygwidgets.SpriteSheetAnimation(self.window, self.getLoc(), 'images/fire/sFire_strip3_smaller.png',
                                                              3, 27, 27, 0.2, loop=True, autoStart=True)

    def setNotAflame(self):
        self.aflame = False

    def replace(self, carName):
        self.oImageCollection.replace(carName)

    def setCameraSpeed(self, newCameraSpeed):
        self.cameraSpeed = newCameraSpeed

    def getCameraSpeed(self):
        return self.cameraSpeed

