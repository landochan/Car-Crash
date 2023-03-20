import pyghelpers
import pygwidgets
from pygame.locals import *
from Constants import *

class Introduction(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.oIntroDisplay = pygwidgets.DisplayText(self.window, (0, 50), value='',
                                                  fontSize=30, width=WINDOWWIDTH,
                                                  textColor=WHITE, justified='center')
        self.oInfo = pygwidgets.DisplayText(self.window, (0, 570), 'Press Space to continue', width=WINDOWWIDTH,
                                            justified='center', fontSize=32, textColor=WHITE)
        self.oByText = pygwidgets.DisplayText(self.window, (0, 600), '© Lando Chan', width=WINDOWWIDTH, justified='center', fontSize=32,
                                              textColor=WHITE)
        self.oInfo.hide()
        self.oByText.hide()
        self.oTimer = pyghelpers.CountDownTimer(2)
        self.oTimer.start()


        try:
            self.file = open('Introduction.txt', 'r')
        except FileNotFoundError:
            return

        self.transfromText()
        self.file.close()

    def transfromText(self):
        textLines = []
        for line in self.file.readlines():
            line = line.strip('\n')
            textLines.append(line)
        self.oIntroDisplay.setText(textLines)

    def getSceneKey(self):
        return INTRODUCTION_SCENE

    def draw(self):
        self.window.fill(BLACK)
        self.oIntroDisplay.draw()
        self.oInfo.draw()
        self.oByText.draw()

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.goToScene(SPLASH_SCENE)

    def update(self):
        if self.oTimer.getTime() == 0.0:
            self.oInfo.show()
            self.oByText.show()
