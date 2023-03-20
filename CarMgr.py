from Constants import *
import random
import pyghelpers
import pygame
from Car import *

class CarMgr():
    CAR_CHOICES = [CAR_RED, CAR_YELLOW, CAR_BLUE, CAR_GREEN]
    pygame.mixer.init()
    CRASH_SOUND = pygame.mixer.Sound('sounds/qubodup-crash.ogg')
    def __init__(self, window, cameraSpeed, oPlayer, oTimer):
        self.window = window
        self.cameraSpeed = cameraSpeed
        self.oPlayerCar = oPlayer.getCar()
        self.carsList = []
        self.oTimer = oTimer


    def addNewCar(self):
        pass

    def deleteUnusedCar(self):
        for oCar in self.carsList:
            locY = oCar.getLoc()[1]
            if (locY > 2 * WINDOWHEIGHT) or (locY < -WINDOWHEIGHT - CAR_HEIGHT):
                self.carsList.remove(oCar)


    def update(self):
        self.deleteUnusedCar()
        self.addNewCar()
        self.checkCollisions()

    def checkCollisions(self):
        for car in self.carsList:
            for otherCar in self.carsList:
                if car == otherCar:
                    continue
                if car.collideCar(otherCar):
                    car.setSpeed((0, 0))
                    otherCar.setSpeed((0, 0))
                    if not car.getAflame():
                        CarMgr.CRASH_SOUND.play()
                    car.setAflame()
                    otherCar.setAflame()
                    #CarMgr.CRASH_SOUND.play()
            if car.collideCar(self.oPlayerCar):
                car.setSpeed((0, 0))
                self.oPlayerCar.setSpeed((0, 0))
                if not car.getAflame() or not self.oPlayerCar.getAflame():
                    CarMgr.CRASH_SOUND.play()
                car.setAflame()
                self.oPlayerCar.setAflame()
                CarMgr.CRASH_SOUND.play()
            car.update()
            car.updateFlame()


    def updateFlame(self):
        for car in self.carsList:
            car.updateFlame()

    def draw(self):
        for car in self.carsList:
            car.draw()

        for car in self.carsList:
            car.drawFlame()

    def reset(self):
        self.carsList = []

    def setCameraSpeed(self, newCameraSpeed):
        for oCar in self.carsList:
            oCar.setCameraSpeed(newCameraSpeed)
        self.cameraSpeed = newCameraSpeed

    def getCameraSpeed(self):
        return self.cameraSpeed



