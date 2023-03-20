import pyghelpers
import pygwidgets
import pygame
from Constants import *
from pygame.locals import *

class Pick(pyghelpers.Scene):
    CARNAME = ['', CAR_RED, CAR_BLUE, CAR_GREEN, CAR_YELLOW, '']
    CARDICT = {CAR_RED: pygame.image.load('images/cars/enlarged_cars_racer_red.png'),
               CAR_BLUE: pygame.image.load('images/cars/enlarged_cars_racer_blue.png'),
               CAR_GREEN: pygame.image.load('images/cars/enlarged_cars_racer_green.png'),
               CAR_YELLOW: pygame.image.load('images/cars/enlarged_cars_racer_yellow.png')}
    CARDICT_TRANSPARENT = {CAR_RED: pygame.image.load('images/cars/enlarged_cars_racer_red.png'),
                           CAR_BLUE: pygame.image.load('images/cars/enlarged_cars_racer_blue.png'),
                           CAR_GREEN: pygame.image.load('images/cars/enlarged_cars_racer_green.png'),
                           CAR_YELLOW: pygame.image.load('images/cars/enlarged_cars_racer_yellow.png')}
    for image in CARDICT_TRANSPARENT.values():
        image.set_alpha(100)

    CARNUM = len(CARDICT)

    def __init__(self, window):
        self.window = window
        self.oTitle = pygwidgets.DisplayText(self.window, (0, 50), value='Pick Your Car', fontSize=50,
                                             width=WINDOWWIDTH, textColor=(255, 0, 0), justified='center')
        #self.oLeftCarName = pygwidgets.DisplayText(self.window, ())
        self.highlightIndex = 1
        self.rotateRate = 5
        self.nextScene = PLAY_SCENE
        self.oLeftImageCollection = pygwidgets.ImageCollection(self.window, (165, 210), Pick.CARDICT_TRANSPARENT, Pick.CARNAME[self.highlightIndex])
        self.oLeftImageCollection.replace('')
        self.oMiddleImageCollection = pygwidgets.ImageCollection(self.window, (285, 200), Pick.CARDICT, Pick.CARNAME[self.highlightIndex])
        self.oRightImageCollection = pygwidgets.ImageCollection(self.window, (405, 210), Pick.CARDICT_TRANSPARENT, Pick.CARNAME[self.highlightIndex + 1])
        self.oTempTimer = pyghelpers.CountDownTimer(2)
        self.oTempTimer.start()
        self.oRightImageCollection.scale(80, scaleFromCenter=True)
        self.oLeftImageCollection.scale(80, scaleFromCenter=True)
        self.oRightArrow = pygwidgets.CustomButton(self.window, (350, 400), up='images/arrows/right_up.png',
                                                   down='images/arrows/right_down.png',
                                                   over='images/arrows/right_over.png',
                                                   disabled='images/arrows/right_disabled.png')
        self.oLeftArrow = pygwidgets.CustomButton(self.window, (200, 400), up='images/arrows/left_up.png',
                                                  down='images/arrows/left_down.png',
                                                  over='images/arrows/left_over.png',
                                                  disabled='images/arrows/left_disabled.png')
        self.oLeftArrow.disable()
        self.okButton = pygwidgets.TextButton(self.window, (250, 500), text='OK', enterToActivate=True)

    def update(self):
        self.oLeftImageCollection.rotate(self.rotateRate)
        self.oRightImageCollection.rotate(self.rotateRate)
        self.oMiddleImageCollection.rotate(self.rotateRate)

    def update_replace(self):
        self.oLeftImageCollection.replace(Pick.CARNAME[self.highlightIndex - 1])
        self.oMiddleImageCollection.replace(Pick.CARNAME[self.highlightIndex])
        self.oRightImageCollection.replace(Pick.CARNAME[self.highlightIndex + 1])

    def getSceneKey(self):
        return PICK_SCENE

    def draw(self):
        self.window.fill('white')
        self.oTitle.draw()
        #self.oLeftCarName.draw()
        self.oLeftImageCollection.draw()
        self.oMiddleImageCollection.draw()
        self.oRightImageCollection.draw()
        pygame.draw.circle(self.window, (200, 200, 200), (285 + (2 * CAR_WIDTH) // 2, 200 + (2 * CAR_HEIGHT) // 2),
                           15 + (2 * CAR_HEIGHT) // 2, 10)
        self.oRightArrow.draw()
        self.oLeftArrow.draw()
        self.okButton.draw()

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.oRightArrow.getEnabled() and (self.oRightArrow.handleEvent(event) or (event.type == KEYDOWN and event.key == K_RIGHT)):
                if self.highlightIndex == 1:
                    self.oLeftArrow.enable()
                self.highlightIndex += 1
                self.update_replace()
                if self.highlightIndex == len(Pick.CARDICT):
                    self.oRightArrow.disable()

            if self.oLeftArrow.getEnabled() and (self.oLeftArrow.handleEvent(event) or (event.type == KEYDOWN and event.key == K_LEFT)):
                if self.highlightIndex == len(Pick.CARDICT):
                    self.oRightArrow.enable()
                self.highlightIndex -= 1
                self.update_replace()
                if self.highlightIndex == 1:
                    self.oLeftArrow.disable()

            if self.okButton.handleEvent(event):
                data = {'carName': Pick.CARNAME[self.highlightIndex], 'message': self.message}
                self.goToScene(self.nextScene, data)

    def enter(self, data):
        self.nextScene = data['nextScene']
        self.message = data['message']

        