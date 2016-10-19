class Word:
    size = 0
    domain = []
    word = []

    def __init__(self, length, word):
        self.word = word.strip()
        self.size = length
        self.domain = createDomain(self.word[0])

def createDomain(start_letter):
    orientations = ['H', 'V']
    domain = []
    temp = []
    for y in range(0,9):
        for x in range(0, 9):
            for orien in orientations:
                if x == 8 and orien == 'H':
                    pass
                elif y == 8 and orien == 'V':
                    pass
                elif [x, y, start_letter] in startingLetters:
                    pass
                else:
                    temp = [x, y, orien]
                    domain.append(temp)
    return domain
                    


mazeMatrix = []
startingLetters = []
words = []

with open('grid1.txt') as mazeText:
    y = 0
    for line in mazeText:
        line = line.strip()
        mazeLine = []
        for x in range(0,len(line)):
            mazeLine.append(line[x])
            if(line[x]!="_"):
                letter = [x, y, line[x]]
                startingLetters.append(letter)
        mazeMatrix.append(line)
        y+=1

with open('bank1.txt') as wordText:
    for line in wordText:
        word = Word(len(line), line.lower())
        words.append(word)
        print(word.domain)

print(mazeMatrix)
print(startingLetters)

