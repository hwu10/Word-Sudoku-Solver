def init():
    mazeMatrix = [] #mazeMatrix is [y][x] i.e. mazeMatrix[3][0] gives us (0, 3)
    startingLetters = []
    words = []
    stateStack = []
    with open('gridtest.txt') as mazeText:
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
       

def sudoku_solver(puzzle, words, stack, err):
    if err == -2:
        return -2
    if err == -1:
        prevState = stack.pop()
        puzzle = prevState.puzzle
        words = prevState.wordList
        #Find the next word to insert and its index
        wordTuple = getNextVariable(words)
        nextWord = wordTuple[0]
        nextWordIndex = wordTuple[1]
        #Find the word's next valid value and its index
        valueTuple = findWordFit(puzzle, wordTuple[0])
        valueFound = valueTuple[0]
        valueFoundIndex = valueTuple[1]
        #Push the found value to the end of the domain
        del nextWord.domain[valueFoundIndex]
        nextWord.domain.append(valueFound)
        words[nextWordIndex] = nextWord
        err = 0
        return sudoku_solver(puzzle, words, stack, err)
    if err == 1:
        return puzzle
    if err == 0:
        if checkIfFilled(puzzle) == True:
            err = 1
            sudoku_solver(puzzle, words, stack, err)
        #Find the next word to insert and its index
        wordTuple = getNextVariable(words)
        nextWord = wordTuple[0]
        nextWordIndex = wordTuple[1]
        #Find the word's next valid value and its index
        valueTuple = findWordFit(puzzle, wordTuple[0])
        valueFound = valueTuple[0]
        #Save the state of the game and push it onto the state stack
        currState = State(words, puzzle)
        stack.append(currState)
        #Insert word into Sudoku
        puzzle = insertWord(puzzle, nextWord.word, valueFound)
        word[nextWordIndex].placed = True
        word[nextWordIndex].domain = [valueFound]
        for i in range(0, len(words)):  
            if (words[i].word != nextWord.word):
                words[i].domain = pruneDomain(words[i]) 
        return sudoku_solver(puzzle, words, stack, err)

class State:
    wordList = []
    puzzle = []
    completed = False

    def __init__(self, words, state):
        self.wordList = words
        self.puzzle = state
        self.completed = False

class Word:
    size = 0
    domain = []
    word = []
    placed = None

    def __init__(self, length, word):
        self.word = word.strip()
        self.size = length
        self.domain = createDomain(self.word[0])
        self.placed = False

def checkIfFilled(puzzle):
    for y in range(0,9):
        for x in range(0,9):
            if puzzle[x][y] == '_':
                return False
    return True


def createDomain(start_letter):
    orientations = ['H', 'V']
    domain = []
    temp = []
    for y in range(0,9):
        for x in range(0, 9):
            for orien in orientations:
                if [x, y, start_letter] in startingLetters:
                    pass
                else:
                    temp = [x, y, orien]
                    domain.append(temp)
    return domain
      
#Ensure that 
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

def insertWord(puzzle, word, value):
    if value[2] == 'H'
        insertx = value[0]
        inserty = value[1]
        for char in word:
            puzzle[insertx][inserty] = char
            insertx += 1

    if value[2] == 'V'
        insertx = value[0]
        inserty = value[1]
        for char in word:
            puzzle[insertx][inserty] = char
            inserty += 1
    return puzzle

#Find the next variable to assign value to
#Prioritize on whether word has fewer than 4 values left in domain
#or if not, chose the word with the longest word size
def getNextVariable(words):
    words.sort(key= lambda x: x.size, reverse=True)
    maxLength = 0
    longestWord = None
    count = 0
    #Words are sorted in descending order of length
    for word in words:
        #First check if the domain has less than four possible values
        if word.placed == True:
            continue
        if len(word.domain) < 4:
            longestWord = word
            break
        #Second check if the word is longer than the current longest
        elif word.size > maxLength:
            longestWord = word
            maxLength = word.size
        #IF same length, use domain size to break tie
        elif word.size == maxLength:
            if len(word.domain) > len(longestWord.domain):
                longestWord = word
        count += 1
    return (longestWord, count)

#Given word and possible word starting point,
#check whether location is valid and if the word
#results in illegal duplicates in rows, columns, and 3x3 boxes
def doesWordFit(sudoku, word, domain):
    count = 0
    if domain[2] == 'H':
        #Ensure no duplicate letters in horizontal row and if word fits
        for x in range(0, 9):
            if x in range(domain[0], domain[0]+word.size):
                if sudoku[domain[1]][x] != '_' and sudoku[domain[1]][x] != word.word[count]:
                    return False
            if sudoku[domain[1]][x] in list(word.word):
                return False
        count += 1
        #Check 3x3 box that each char in the word is in
        charx = domain[0]
        chary = domain[1]
        for char in word.word:
            for x in range(charx - charx%3, charx - charx%3 + 3):
                for y in range(chary - chary%3, chary - chary%3 + 3):
                    if sudoku[x][y] == char:
                        return False
            charx += 1

    elif domain[2] == 'V':
        #Ensure no duplicate letters in vertical row and if word fits
        for y in range(0, 9):
            if y in range(domain[0], domain[0]+word.size):
                if sudoku[domain[1]][y] != '_' and sudoku[domain[1]][y] != word.word[count]:
                    return False
            if sudoku[domain[1]][y] in list(word.word):
                return False
        count += 1
        #Check 3x3 box that each char in the word is in
        charx = domain[0]
        chary = domain[1]
        for char in word.word:
            for x in range(charx - charx%3, charx - charx%3 +3):
                for y in range(chary - chary%3, chary - chary%3 +3):
                    if sudoku[x][y] == char:
                        return False
            chary += 1
    return True

def findWordFit(puzzle, word):
    index = 0
    for value in word.domain:
        if doesWordFit(puzzle, word, value) == True:
            return (value, index)
        index += 1
    return False

init()
