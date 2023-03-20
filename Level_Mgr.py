import pyghelpers
import pygwidgets
from pathlib import *
from Constants import *

class Level_Mgr(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.oTitle = pygwidgets.DisplayText(self.window, (0, 50), value='Levels', fontSize=100,
                                             width=WINDOWWIDTH, justified='center', textColor=RED)
        self.oMenuButton = pygwidgets.TextButton(self.window, (20, 20), 'Menu',
                                                 width=100, height=30)
        self.oLevelButtonList = []
        self.oLevelDict = {}

        try:
            self.file = open('levels.txt', 'r')
        except FileNotFoundError:
            return

        self.transformData()
        # self.printLevel()
        self.file.close()

        top = 200
        for key in self.oLevelDict.keys():
            oButton = pygwidgets.TextButton(self.window, (BUTTONLEFTMARGIN - BUTTONWIDTH, top), key, width=BUTTONWIDTH*3,
                                            height=50, fontSize=32, nickname=key, callBack=self.levelButtonCallback)
            self.oLevelButtonList.append(oButton)
            top += 75

    def levelButtonCallback(self, nickname):
        data = {'nextScene': LEVEL_SCENE, 'message': self.oLevelDict[nickname]}
        self.goToScene(PICK_SCENE, data)

    # For debug
    def printLevel(self):
        for key in self.oLevelDict.keys():
            print(key)
            print(self.oLevelDict[key])
            print()


    def transformData(self):
        dataLines = self.file.readlines()

        newLevel = False
        startingPos = False
        cameraSpeed = False
        newTime = False
        for dataLine in dataLines:
            if dataLine == '\n':
                if newTime:
                    newLevel = True
                else:
                    newTime = True
                continue
            dataLine = dataLine.strip('\n')
            if dataLine[0] == '#':
                continue
            elif newLevel:
                levelName = dataLine
                self.oLevelDict[levelName] = []
                newLevel = False
                startingPos = True
            elif startingPos:
                dataLine = dataLine.split(', ')
                startingLoc = (int(dataLine[0]), int(dataLine[1]))
                self.oLevelDict[levelName].append(startingLoc)
                startingPos = False
                cameraSpeed = True
            elif cameraSpeed:
                speed = int(dataLine)
                self.oLevelDict[levelName].append(speed)
                cameraSpeed = False
            elif newTime:
                self.oLevelDict[levelName].append([float(dataLine)])
                newTime = False
            else:
                dataLine = dataLine.split(', ')
                dataLine = [float(dataLine[0]), float(dataLine[1]), float(dataLine[2]), dataLine[3]]
                self.oLevelDict[levelName][-1].append(dataLine)


    def getSceneKey(self):
        return LEVEL_MGR_SCENE

    def draw(self):
        self.window.fill(WHITE)
        self.oTitle.draw()
        self.oMenuButton.draw()
        for oButton in self.oLevelButtonList:
            oButton.draw()

    def update(self):
        pass

    def handleInputs(self, events, keyPressedList):
        for event in events:
            for oButton in self.oLevelButtonList:
                oButton.handleEvent(event)
            if self.oMenuButton.handleEvent(event):
                self.goToScene(SPLASH_SCENE)