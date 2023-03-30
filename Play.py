import pygame
import sys
import pyghelpers
import pygwidgets

from Constants import *
from Background import *
from ClassicCarMgr import *
from Player import *

STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'
STATE_PENDING = 'pending'

class Play(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.oTimer = pyghelpers.CountUpTimer()
        self.oSpeedTimer = pyghelpers.CountUpTimer()
        self.cameraSpeed = 10
        self.carNum = 5
        self.carMaxSpeed = 10
        self.playerMaxSpeed = 15
        self.playerSpeedX = 5
        startLocX = (WINDOWWIDTH - CAR_WIDTH) // 2
        startLocY = HALFWINDOWHEIGHT + 200
        self.oBackgroundMgr = BackgroundMgr(self.window, self.cameraSpeed, 155)
        self.oPlayer = Player(self.window, (startLocX, startLocY), self.playerSpeedX)
        self.oCarMgr = ClassicCarMgr(self.window, self.cameraSpeed, self.oPlayer, self.oTimer, self.carNum,
                                     self.carMaxSpeed + 1)
        self.oCarMgr.setAddRate(1.0)
        self.oNewGameButton = pygwidgets.TextButton(self.window, (20, 70), 'New Game',
                                                      width=100, height=30, enterToActivate=True)
        self.oChangeCarButton = pygwidgets.TextButton(self.window, (20, 110), 'Change Car',
                                                      width=100, height=30)
        self.oMenuButton = pygwidgets.TextButton(self.window, (20, 150), 'Menu',
                                                 width = 100, height=30)
        self.oHighestScoreDisplay = pygwidgets.DisplayText(self.window, (20, 50), '', fontSize=20, textColor=WHITE)
        self.score = 0
        self.oScoreDisplay = pygwidgets.DisplayText(self.window, (20, 20), value='Score: 0',
                                                    fontSize=40, textColor=WHITE)
        self.oGameOverDisplay = pygwidgets.DisplayText(self.window, (0, 100), value='GAME OVER',
                                                       fontSize=50, width=WINDOWWIDTH, textColor=RED,
                                                       justified='center')
        self.oScoreCountDownTimer = pyghelpers.CountDownTimer(0.5)
        self.playing_state = STATE_PENDING
        # self.oBackgroundMgr.hide()

    def getSceneKey(self):
        return PLAY_SCENE

    def update(self):
        if self.playing_state == STATE_PLAYING:
            self.oBackgroundMgr.update()
            self.oCarMgr.update()
            self.oPlayer.update()
            currentScore = int(self.oBackgroundMgr.getDistance() / 100)
            if currentScore > self.score:
                self.score = currentScore
                self.oScoreDisplay.setValue('Score: %s' %self.score)

            if self.score > 51200:
                self.oCarMgr.setAddRate(0.1)
            elif self.score > 25600:
                self.oCarMgr.setAddRate(0.2)
            elif self.score > 12800:
                self.oCarMgr.setAddRate(0.3)
            elif self.score > 6400:
                self.oCarMgr.setAddRate(0.4)
            elif self.score > 3200:
                self.oCarMgr.setAddRate(0.5)
            elif self.score > 1600:
                self.oCarMgr.setAddRate(0.6)
            elif self.score > 800:
                self.oCarMgr.setAddRate(0.7)
            elif self.score > 400:
                self.oCarMgr.setAddRate(0.8)
            elif self.score > 200:
                self.oCarMgr.setAddRate(0.9)


            if self.oPlayer.getAflame():
                pygame.mixer.music.stop()
                self.playing_state = STATE_GAME_OVER
                self.oTimer.stop()
                pygame.mouse.set_visible(True)
                self.oScoreCountDownTimer.stop()
                self.draw()
                if self.score > self.lowestScore:
                    results = pyghelpers.textYesNoDialog(self.window, (HALFWINDOWWIDTH - 200, 100, 400, 150),
                                                         prompt='Your score %s is a new highscore!\n Go to Highscore panel and record your name!' %self.score,
                                                         yesButtonText='Save Highscore', noButtonText='Cancel', backgroundColor=(255, 255, 0))
                    if results:
                        self.goToScene(HIGHSCORE_SCENE, [PLAY_SCENE, self.score])
                self.oNewGameButton.enable()
                self.oChangeCarButton.enable()
                self.oMenuButton.enable()


        elif self.playing_state == STATE_GAME_OVER:
            self.oPlayer.updateFlame()
            self.oCarMgr.updateFlame()
                
            

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if self.oNewGameButton.handleEvent(event):
                self.playing_state = STATE_PLAYING
                self.reset()
                self.oNewGameButton.disable()
                self.oChangeCarButton.disable()
                self.oMenuButton.disable()
                self.oTimer.start()
                self.oSpeedTimer.start()
                pygame.mouse.set_visible(False)
                pygame.mixer.music.play(-1)

            if self.oChangeCarButton.handleEvent(event):
                self.playing_state = STATE_PENDING
                self.reset()
                data = {'nextScene': PLAY_SCENE, 'message': None}
                self.goToScene(PICK_SCENE, data)

            if self.oMenuButton.handleEvent(event):
                self.goToScene(SPLASH_SCENE)

        if self.playing_state == STATE_PLAYING:
            self.oPlayer.handleEvents(keyPressedList)
            if self.oSpeedTimer.getTime() < 0.2:
                return
            self.oSpeedTimer.start()
            if (keyPressedList[K_UP] or keyPressedList[K_w]) and self.cameraSpeed < self.playerMaxSpeed:
                self.cameraSpeed += 1
            elif (keyPressedList[K_DOWN] or keyPressedList[K_s]) and self.cameraSpeed > -self.playerMaxSpeed:
                self.cameraSpeed -= 1
            if self.cameraSpeed > 0.2:
                self.cameraSpeed -= 0.2
            elif self.cameraSpeed < -0.2:
                self.cameraSpeed += 0.2
            self.setCameraSpeed()


    def setCameraSpeed(self):
        self.oCarMgr.setCameraSpeed(self.cameraSpeed)
        self.oBackgroundMgr.setCameraSpeed(self.cameraSpeed)


    def reset(self):
        self.oPlayer.reset()
        self.oCarMgr.reset()
        self.oBackgroundMgr.reset()
        self.cameraSpeed = 0
        self.setCameraSpeed()
        self.score = 0
        self.oScoreDisplay.setValue('Score: %s' % self.score)
        self.oScoreCountDownTimer.start()

    def draw(self):
        self.window.fill('black')
        self.oBackgroundMgr.draw()
        self.oCarMgr.draw()
        self.oPlayer.draw()
        self.oScoreDisplay.draw()
        self.oNewGameButton.draw()
        self.oChangeCarButton.draw()
        self.oMenuButton.draw()
        self.oHighestScoreDisplay.draw()
        
        if self.playing_state == STATE_GAME_OVER:
            self.oGameOverDisplay.draw()

    def enter(self, data):
        if data['carName'] != None:
            self.oPlayer.replace(data['carName'])

        self.highestScore, self.lowestScore = self.request(HIGHSCORE_SCENE, ASK_HIGHSCORE)
        self.oHighestScoreDisplay.setValue('Highest Score: %s' %self.highestScore)
        pygame.mixer.music.load('sounds/The Rush.mp3')


