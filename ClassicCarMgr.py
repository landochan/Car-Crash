from CarMgr import *

class ClassicCarMgr(CarMgr):
    def __init__(self, window, cameraSpeed, oPlayer, oTimer, carNum, carMaxSpeed):
        super().__init__(window, cameraSpeed, oPlayer, oTimer)
        self.addRate = 1.0
        self.carNum = carNum
        self.carMaxSpeed = carMaxSpeed

    def setAddRate(self, newAddRate):
        self.addRate = newAddRate

    def getAddRate(self):
        return self.addRate

    def addNewCar(self):
        if self.oTimer.getTime() > self.addRate:
            self.oTimer.start()
            choice = random.choice(CarMgr.CAR_CHOICES)
            colliding = True
            while colliding:
                locX = random.randint(LEFTMARGIN, RIGHTMARGIN - CAR_WIDTH)
                speedY = random.randint(-self.carMaxSpeed, self.carMaxSpeed)
                # speedY = CAMERA_SPEED // 2
                if speedY == - self.cameraSpeed:
                    continue

                direction = 'front'
                if speedY > 0:
                    direction = 'back'

                if speedY + self.cameraSpeed > 0:
                    locY = random.randint(-WINDOWHEIGHT, -CAR_HEIGHT)
                else:
                    locY = random.randint(WINDOWHEIGHT, 2 * WINDOWHEIGHT - CAR_HEIGHT)

                loc = [locX, locY]
                speed = [0, speedY]
                instanceCar = Car(self.window, loc, speed, choice, self.cameraSpeed, direction)
                colliding = False
                for otherCar in self.carsList:
                    if instanceCar.collideCar(otherCar):
                        colliding = True
                        break

            self.carsList.append(instanceCar)

