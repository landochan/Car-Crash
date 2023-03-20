import pygame
import pyghelpers
import pygwidgets
from Constants import *
from Background import *
from Player import *
from LevelCarMgr import *

class Level(pyghelpers.Scene):
    STATUS_PLAYING = 'playing status'
    STATUS_PENDING = 'pending status'
    STATUS_GAMEOVER = 'game over status'
    STATUS_FINISH = 'finish status'
    def __init__(self, window):
        self.window = window
        self.cameraSpeed = 10
        self.playerSpeedX = 5
        self.carName = CAR_RED
        self.levelData = None
        self.oTimer = pyghelpers.CountUpTimer()
        self.oPlayer = Player(self.window, (0, 0), self.playerSpeedX)
        self.oCarMgr = LevelCarMgr(self.window, self.cameraSpeed, self.oPlayer, self.oTimer)
        self.oBackgroundMgr = BackgroundMgr(self.window, self.cameraSpeed, 155)
        self.oStartButton = pygwidgets.TextButton(self.window, (20, 20), 'Start',
                                                  width=100, height=30)
        self.oRetryButton = pygwidgets.TextButton(self.window, (20, 20), 'Retry',
                                                  width=100, height=30)
        self.oChangeCarButton = pygwidgets.TextButton(self.window, (20, 60), 'Change Car',
                                                      width=100, height=30)
        self.oLevelsButton = pygwidgets.TextButton(self.window, (20, 100), 'Levels',
                                                 width=100, height=30)
        self.oMenuButton = pygwidgets.TextButton(self.window, (20, 140), 'Main Menu',
                                                 width=100, height=30)
        self.oGameOverDisplay = pygwidgets.DisplayText(self.window, (0, 100), value='GAME OVER',
                                                       fontSize=50, width=WINDOWWIDTH, textColor=RED,
                                                       justified='center')
        self.oFinishDisplay = pygwidgets.DisplayText(self.window, (0, 100), value='FINISH',
                                                     fontSize=50, width=WINDOWWIDTH, textColor=GREEN,
                                                     justified='center')
        self.endTime = 0.0
        self.playing_state = Level.STATUS_PENDING


    def draw(self):
        self.window.fill(BLACK)
        self.oBackgroundMgr.draw()
        self.oCarMgr.draw()
        self.oPlayer.draw()
        self.oStartButton.draw()
        self.oRetryButton.draw()
        self.oChangeCarButton.draw()
        self.oLevelsButton.draw()
        self.oMenuButton.draw()

        if self.playing_state == Level.STATUS_GAMEOVER:
            self.oGameOverDisplay.draw()

        elif self.playing_state == Level.STATUS_FINISH:
            self.oFinishDisplay.draw()

    def enter(self, data):
        self.oStartButton.show()
        self.oStartButton.enable()
        self.oRetryButton.hide()
        self.carName = data['carName']
        self.levelData = data['message']
        dataLen = len(self.levelData)
        self.oCarMgr.setLevelData(self.levelData[2:dataLen-1])
        self.prepareGame()
        pygame.mixer.music.load('sounds/The Rush.mp3')

    def leave(self):
        self.reset()
        pygame.mixer.music.stop()

    def prepareGame(self):
        self.oPlayer.replace(self.carName)
        self.cameraSpeed = self.levelData[1]
        self.setCameraSpeed()
        self.startLoc = self.levelData[0]
        self.oPlayer.setLoc(self.startLoc)
        self.endTime = self.levelData[-1][0]

    def setCameraSpeed(self):
        self.oCarMgr.setCameraSpeed(self.cameraSpeed)
        self.oBackgroundMgr.setCameraSpeed(self.cameraSpeed)


    def update(self):
        if self.playing_state == Level.STATUS_PLAYING:
            self.oBackgroundMgr.update()
            self.oCarMgr.update()
            self.oPlayer.update()

            if self.oPlayer.getAflame():
                self.playing_state = Level.STATUS_GAMEOVER
                self.oTimer.stop()
                pygame.mouse.set_visible(True)
                self.oRetryButton.enable()
                self.oLevelsButton.enable()
                self.oMenuButton.enable()
                self.oChangeCarButton.enable()
                pygame.mixer.music.stop()

            if self.oTimer.getTime() > self.endTime:
                self.playing_state = Level.STATUS_FINISH
                self.oRetryButton.enable()
                self.oLevelsButton.enable()
                self.oMenuButton.enable()
                self.oChangeCarButton.enable()
                pygame.mouse.set_visible(True)

        elif self.playing_state in [Level.STATUS_GAMEOVER, Level.STATUS_FINISH]:
            self.oCarMgr.updateFlame()
            self.oPlayer.updateFlame()


    def getSceneKey(self):
        return LEVEL_SCENE

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.oLevelsButton.handleEvent(event):
                self.goToScene(LEVEL_MGR_SCENE)
            if self.oStartButton.handleEvent(event) or self.oRetryButton.handleEvent(event):
                self.oTimer.start()
                self.reset()
                self.playing_state = Level.STATUS_PLAYING
                self.oRetryButton.show()
                self.oStartButton.hide()
                self.oStartButton.disable()
                self.oRetryButton.disable()
                self.oLevelsButton.disable()
                self.oMenuButton.disable()
                self.oChangeCarButton.disable()
                pygame.mouse.set_visible(False)
                pygame.mixer.music.play(-1)
            if self.oMenuButton.handleEvent(event):
                self.goToScene(SPLASH_SCENE)
            if self.oChangeCarButton.handleEvent(event):
                self.playing_state = Level.STATUS_PENDING
                self.reset()
                data = {'nextScene': LEVEL_SCENE, 'message': self.levelData}
                self.goToScene(PICK_SCENE, data)

        if self.playing_state == Level.STATUS_PLAYING:
            self.oPlayer.handleEvents(keyPressedList)


    def reset(self):
        self.playing_state = Level.STATUS_PENDING
        self.oCarMgr.reset()
        self.oPlayer.reset()
        self.oPlayer.setLoc(self.startLoc)

