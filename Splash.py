import pyghelpers
import pygwidgets
import pygame, sys
from Constants import *
from pygame.locals import *

class Splash(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.oTitle = pygwidgets.DisplayText(self.window, (0, 50), value='Car Crash', fontName='jokerman',
                                             fontSize=100, width=WINDOWWIDTH, justified='center', textColor=(255, 0, 0))
        self.oClassicButton = pygwidgets.TextButton(self.window, (BUTTONLEFTMARGIN, 200), 'Classic', width=BUTTONWIDTH, height=50, fontSize=32)
        self.oLevelsButton = pygwidgets.TextButton(self.window, (BUTTONLEFTMARGIN, 275), 'Levels', width=BUTTONWIDTH, height=50, fontSize=32)
        self.oHighscoreButton = pygwidgets.TextButton(self.window, (BUTTONLEFTMARGIN, 350), 'Highscores', width=BUTTONWIDTH, height=50, fontSize=32)
        self.oCreditsButton = pygwidgets.TextButton(self.window, (BUTTONLEFTMARGIN, 425), 'Credits', width=BUTTONWIDTH, height=50, fontSize=32)
        self.oByText = pygwidgets.DisplayText(self.window, (0, 600), '© Lando Chan', width=WINDOWWIDTH, justified='center', fontSize=32)

    def getSceneKey(self):
        return SPLASH_SCENE

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if self.oClassicButton.handleEvent(event):
                data = {'nextScene': PLAY_SCENE, 'message': None}
                self.goToScene(PICK_SCENE, data)

            if self.oLevelsButton.handleEvent(event):
                self.goToScene(LEVEL_MGR_SCENE)
            
            if self.oHighscoreButton.handleEvent(event):
                self.goToScene(HIGHSCORE_SCENE, [SPLASH_SCENE, None])
            
            if self.oCreditsButton.handleEvent(event):
                self.goToScene(CREDITS_SCENE, SPLASH_SCENE)

    def draw(self):
        self.window.fill('white')
        self.oTitle.draw()
        self.oClassicButton.draw()
        self.oLevelsButton.draw()
        self.oHighscoreButton.draw()
        self.oCreditsButton.draw()
        self.oByText.draw()


