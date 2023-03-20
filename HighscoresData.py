from pathlib import Path
import json
from Constants import *

class HighscoresData():
    def __init__(self):
        self.BLANK_HIGHSCORES_TABLE = [['-----', 0]] * HIGHSCORES_NUM
        self.oFilePath = Path('Highscores.json')

        try:
            data = self.oFilePath.read_text()
        except FileNotFoundError:
            self.resetScores()
            return

        self.highscore = json.loads(data)
        


    def resetScores(self):
        self.highscore = self.BLANK_HIGHSCORES_TABLE

    def save(self):
        data = json.dumps(self.highscore)
        self.oFilePath.write_text(data)


    def getNamesAndScores(self):
        namesList = []
        scoresList = []
        for highscoreItem in self.highscore:
            namesList.append(highscoreItem[0])
            scoresList.append(highscoreItem[1])

        return namesList, scoresList


    def addNew(self, name, highscore):
        if name == None:
            return
        if name == '':
            name = 'Anonymous'

        # Find the index of the highscore
        namesList, scoresList = self.getNamesAndScores()
        scoreIndex = HIGHSCORES_NUM - 1
        while scoreIndex > 0:
            if highscore < scoresList[scoreIndex - 1]:
                break
            scoreIndex -= 1

        self.highscore.insert(scoreIndex, [name, highscore])
        self.highscore.pop()