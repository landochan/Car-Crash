from CarMgr import *
import random

class LevelCarMgr(CarMgr):
    def __init__(self, window, cameraSpeed, oPlayer, oTimer):
        super().__init__(window, cameraSpeed, oPlayer, oTimer)
        self.timeIndex = 0
        self.nextTimeEvent = 0.0

    def setLevelData(self, levelData):
        self.levelData = levelData
        self.reset()

    def addNewCar(self):
        if self.timeIndex == len(self.levelData):
            return
        self.setNextEventTime()
        if self.oTimer.getTime() > self.nextTimeEvent:
            for carInfo in self.levelData[self.timeIndex][1:]:
                loc = (carInfo[0], carInfo[1])
                speed = carInfo[2]
                if speed > 0:
                    direction = 'back'
                else:
                    direction = 'front'
                carName = carInfo[3]
                if carName == 'random':
                    carName = random.choice(CarMgr.CAR_CHOICES)
                oCar = Car(self.window, loc, (0, speed), carName, self.cameraSpeed, direction)
                self.carsList.append(oCar)
            self.timeIndex += 1

    def reset(self):
        super().reset()
        self.timeIndex = 0
        self.setNextEventTime()

    def setNextEventTime(self):
        self.nextTimeEvent = self.levelData[self.timeIndex][0]



