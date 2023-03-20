import pyghelpers
import pygwidgets
import pygame
from Constants import *
from HighscoresData import *

class Highscore(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.returnScene = SPLASH_SCENE
        self.oHighscore = HighscoresData()
        self.oTitle = pygwidgets.DisplayText(self.window, (0, 70), value='Highscores',
                                             fontSize=60, width=WINDOWWIDTH, textColor=(255, 0, 0), justified='center')
        self.oNameDisplay = pygwidgets.DisplayText(self.window, (0, 125), value='Name', width=HALFWINDOWWIDTH,
                                                   fontSize=40, textColor=BLACK, justified='center')
        self.oScoreDisplay = pygwidgets.DisplayText(self.window, (HALFWINDOWWIDTH, 125), value='Score', width=HALFWINDOWWIDTH,
                                                    fontSize=40, textColor=BLACK, justified='center')
        self.oNumberListDisplay = pygwidgets.DisplayText(self.window, (10, 170), value=list(range(1, HIGHSCORES_NUM + 1)),
                                                         fontSize=40, textColor=(100, 100, 100))
        self.oNameListDisplay = pygwidgets.DisplayText(self.window, (60, 170), fontSize=40, textColor=(100, 100, 100))
        self.oScoreListDisplay = pygwidgets.DisplayText(self.window, (40 + HALFWINDOWWIDTH, 170), fontSize=40, textColor=(100, 100, 100))
        self.updateNamesAndScoresDisplay()
        self.oBackButton = pygwidgets.TextButton(self.window, (HALFWINDOWWIDTH + 50, 500), text='Back',
                                                 width=50)
        self.oResetButton = pygwidgets.TextButton(self.window, (HALFWINDOWWIDTH - 100, 500), text='Reset',
                                                  width=50)

    def getSceneKey(self):
        return HIGHSCORE_SCENE

    def draw(self):
        self.window.fill(WHITE)
        self.oTitle.draw()
        self.oNameDisplay.draw()
        self.oScoreDisplay.draw()
        pygame.draw.line(self.window, BLACK, (20, 160), (WINDOWWIDTH - 20, 160))
        # pygame.draw.line(self.window, BLACK, (HALFWINDOWWIDTH, 160), (HALFWINDOWWIDTH, WINDOWHEIGHT - 20))
        self.oNumberListDisplay.draw()
        self.oNameListDisplay.draw()
        self.oScoreListDisplay.draw()
        self.oResetButton.draw()
        self.oBackButton.draw()


    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.oBackButton.handleEvent(event):
                data = {'carName': None}
                self.goToScene(self.returnScene, data)
            if self.oResetButton.handleEvent(event):
                self.oHighscore.resetScores()
                self.updateNamesAndScoresDisplay()
        pass

    def updateNamesAndScoresDisplay(self):
        self.names, self.scores = self.oHighscore.getNamesAndScores()
        self.oNameListDisplay.setValue(self.names)
        self.oScoreListDisplay.setValue(self.scores)

    def enter(self, dataList):
        self.returnScene = dataList[0]
        newHighscore = dataList[1]
        if newHighscore == None:
            return
        self.draw()
        name = pyghelpers.textAnswerDialog(self.window, (HALFWINDOWWIDTH - 200, HALFWINDOWHEIGHT, 400, 200),
                                           'Please insert your name as the holder\n of the new highscore %s' % newHighscore)
        self.oHighscore.addNew(name, newHighscore)
        self.updateNamesAndScoresDisplay()

    def respond(self, requestID):
        if requestID == ASK_HIGHSCORE:
            namesList, scoresList = self.oHighscore.getNamesAndScores()
            return scoresList[0], scoresList[-1]

    def update(self):
        self.updateNamesAndScoresDisplay()
        pass

    def leave(self):
        self.oHighscore.save()





