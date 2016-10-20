mazeMatrix = [] #mazeMatrix is [y][x] i.e. mazeMatrix[3][0] gives us (0, 3)
startingLetters = []
words = []

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
      
def pruneDomain(word):
    matrixMaxY = 9
    matrixMaxX = 9
    removeList = []
    for value in word.domain:
        if value[2] == 'H' and value[0] > matrixMaxX - word.size:
            removeList.append(value)
        elif value[2] == 'V' and value[1] > matrixMaxY - word.size:
            removeList.append(value)
    for value in removeList:
        word.domain.remove(value)
    return word.domain

def getNextVariable(words):
    words.sort(key= lambda x: x.size, reverse=True)
    maxLength = 0
    longestWord = None
    for word in words:
        if len(word.domain) < 4:
            longestWord = word
            break
        elif word.size > maxLength:
            longestWord = word
            maxLength = word.size
        elif word.size == maxLength:
            if len(word.domain) > len(longestWord.domain):
                longestWord = word
    return longestWord

def doesWordFit(sudoku, word, domain):
    count = 0
    if domain[2] == 'H':
        for x in range(domain[0], domain[0]+word.size):
            if sudoku[domain[1]][x] != '_' and sudoku[domain[1]][x] != word.word[count]:
                return False
        count += 1
    elif domain[2] == 'V':
        for y in range(domain[1], domain[1]+word.size):
            if sudoku[y][domain[0]] != '_' and sudoku[y][domain[0]] != word.word[count]:
                return False
        count += 1
    return True

def findWordFit(word):
    for value in word.domain:
        if doesWordFit(mazeMatrix, word, value) == True:
            return value
    return False

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
        line = line.rstrip()
        word = Word(len(line), line.lower())
        word.domain = pruneDomain(word)
        words.append(word)


print(startingLetters)
nextWord = getNextVariable(words)
print(findWordFit(nextWord))
