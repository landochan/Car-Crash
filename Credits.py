import pyghelpers
import pygwidgets
from Constants import *

class Credits(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.oTitle = pygwidgets.DisplayText(self.window, (0, 50), value='Credits', fontSize=100,
                                             width=WINDOWWIDTH, justified='center', textColor=RED)

        try:
            creditsFile = open('Credits.txt', 'r')
            self.data = creditsFile.readlines()
            creditsFile.close()
        except FileNotFoundError:
            self.data = None

        self.oCreditsList = []
        self.processData()

    def processData(self):
        if self.data == None:
            return
        lineCount = 0
        top = 150
        for dataLine in self.data:
            if dataLine[0] == '#':
                continue
            dataLine = dataLine.strip('\n')
            if dataLine == '':
                lineCount = 0
                continue
            if lineCount == 0:
                title, creator, license = dataLine.split(', ')
            elif lineCount == 1:
                assetLink = dataLine
            elif lineCount == 2:
                licenseLink = dataLine
                text = title + ' by ' + creator + ' under ' + license
                oCredits = pygwidgets.DisplayText(self.window, (10, top), value=text, fontSize=24, fontName='Calibri')
                top += 30
                self.oCreditsList.append(oCredits)

            lineCount += 1

        top += 20
        self.detailsText = pygwidgets.DisplayText(self.window, (10, top), value='For links, see Credits.txt',
                                                  fontSize=24, fontName='Calibri')
        top += 30
        self.oBackButton = pygwidgets.TextButton(self.window, (HALFWINDOWWIDTH - 50, top), text='Back')


    def getSceneKey(self):
        return CREDITS_SCENE

    def draw(self):
        self.window.fill(WHITE)
        self.oTitle.draw()
        for oCredits in self.oCreditsList:
            oCredits.draw()
        self.detailsText.draw()
        self.oBackButton.draw()

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.oBackButton.handleEvent(event):
                self.goToScene(SPLASH_SCENE)

