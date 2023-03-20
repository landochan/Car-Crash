x0 = 155
xDict = {'x1': x0 + 20,
         'x2': x0 + 54,
         'x3': x0 + 90,
         'x4': x0 + 125,
         'x5': x0 + 158,
         'x6': x0 + 192,
         'x7': x0 + 228,
         'x8': x0 + 264}
yDict = {'yTop': -55,
         'yBot': 650}
startingPosDict = {'middle': '296, 297',
                   'bottom': '296, 595',
                   'midbottom': '296, 446'}

def convert():
    try:
        raw_file = open('Levels_raw.txt', 'r')
        dest_file = open('Levels.txt', 'w')
    except FileNotFoundError:
        print('File not found')
        return

    data = raw_file.readlines()
    raw_file.close()
    for dataLine in data:
        if dataLine[0] == '#':
            continue
        dataLine = dataLine.split(', ')
        if len(dataLine) == 1:
            dataLine = dataLine[0].strip('\n')
            if dataLine in list(startingPosDict.keys()):
                dataLine = startingPosDict[dataLine]
            dataLine = dataLine + '\n'
            dest_file.writelines(dataLine)
            continue
        xNum = xDict[dataLine[0]]
        yNum = yDict[dataLine[1]]
        dataLine = ', '.join([str(xNum), str(yNum), dataLine[2], dataLine[3]])
        dest_file.writelines(dataLine)

    dest_file.close()

convert()



