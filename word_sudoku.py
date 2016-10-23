import copy

def init():
    puzzle = [] #mazeMatrix is [row][col] 
    startingLetters = []
    words = []
    stateStack = []
    with open('grid1.txt') as mazeText:
        y = 0
        for line in mazeText:
            #Set each maze line to lower case and seperate into list of characters
            line = line.lower()
            line = line.strip()
            mazeLine = []
            for x in range(0,len(line)):
                mazeLine.append(line[x])
                if(line[x]!="_"):
                    letter = [x, y, line[x].lower()]
                    startingLetters.append(letter)
            puzzle.append(mazeLine)
            y+=1

    with open('bank1.txt') as wordText:
        for line in wordText:
            line = line.lower()
            line = line.rstrip()
            word = Word(len(line), line.lower(), startingLetters)
            #Prune domain so that starting positions won't cause word to fall off map
            word.domain = pruneDomain(word)
            words.append(word)

    #Prune domain values that are incompatible with the starting characters on the puzzle
    for i in range(0, len(words)):  
        toDelete = []
        for domainValue in words[i].domain:
            if doesWordFit(puzzle, words[i], domainValue) == False:
                toDelete.append(domainValue)
        for word in toDelete: 
            words[i].domain.remove(word)

    #Keep a copy of the original state on the stateStack
    tempWords = copy.deepcopy(words)
    for i in range(0, len(words)):
        tempDomain = copy.deepcopy(words[i].domain)
        tempWords[i].domain = tempDomain
    currState = State(tempWords, [x[:] for x in puzzle])
    stateStack.append(currState)

    #Solve sudoku
    printSudoku(sudoku_solver(puzzle, words, stateStack, 0))


def sudoku_solver(puzzle, words, stack, err):
    #If puzzle is filled up and all words placed, return success
    if checkIfFilled(puzzle, words) == True:
        err = 1
        return puzzle

    #Previous reccurence had an erro
    if err == -1:
        if len(stack) > 1:
            prevState = stack.pop()
            puzzle = [x[:] for x in prevState.puzzle]
            words = prevState.wordList
        #Find the same word that was found last time
        wordTuple = getNextVariable(words)
        if wordTuple == False:
            err = -1
            return sudoku_solver(puzzle, words, stack, err)
        nextWord = wordTuple[0]
        nextWordIndex = wordTuple[1]

        #If found word has no valid values, return error
        valueTuple = findWordFit(puzzle, wordTuple[0])
        if (valueTuple == False):
            err = -1
            return sudoku_solver(puzzle, words, stack, err)

        err = 0
        return sudoku_solver(puzzle, words, stack, err)

    #Puzzle solution still valid
    if err == 0:
        #Find the next word to insert and its index
        wordTuple = getNextVariable(words)
        nextWord = wordTuple[0]
        nextWordIndex = wordTuple[1]

        #Find the word's next valid value and its index
        valueTuple = findWordFit(puzzle, wordTuple[0])
        if (valueTuple == False):
            err = -1
            return sudoku_solver(puzzle, words, stack, err)
        valueFound = valueTuple[0]
        valueIndex = valueTuple[1]
        
        #Even if word location doesn't work, mark domain value's checked flag as True so we don't look for it again
        words[nextWordIndex].domain[valueIndex][3] = True 
        #Save the state of the game and push it onto the state stack
        tempWords = copy.deepcopy(words)
        for i in range(0, len(words)):
            tempDomain = copy.deepcopy(words[i].domain)
            tempWords[i].domain = tempDomain
        currState = State(tempWords, [x[:] for x in puzzle])
        stack.append(currState)

        #Insert word into Sudoku
        puzzle = [x[:] for x in insertWord(puzzle, nextWord.word, valueFound)]
        words[nextWordIndex].placed = True
        words[nextWordIndex].domain = [valueFound]

        #Prune domains of all words that aren't already placed
        for i in range(0, len(words)):  
            if (words[i].placed != True):
                toDelete = []
                for domainValue in words[i].domain:
                    if doesWordFit(puzzle, words[i], domainValue) == False:
                        toDelete.append(domainValue)
                for word in toDelete: 
                    words[i].domain.remove(word)
            if len(words[i].domain) == 0:
                err = -1
                words[nextWordIndex].placed = False
                break
        return sudoku_solver(puzzle, words, stack, err)

#State of the puzzle
class State:
    wordList = []
    puzzle = []
    completed = False
    
    def __init__(self, words, state):
        self.wordList = words
        self.puzzle = state
        self.completed = False

#Word class
class Word:
    size = 0
    domain = []
    word = []
    placed = None
    skip = None

    def __init__(self, length, word, startingLetters):
        self.word = word.strip()
        self.size = length
        self.domain = createDomain(self.word[0], startingLetters)
        self.placed = False
        self.skip = False
     
def checkIfFilled(puzzle, words):
    for y in range(0,9):
        for x in range(0,9):
            if puzzle[y][x] == '_':
                return False
    for word in words:
        if word.placed == False:
            return False
    return True

def createDomain(start_letter, startingLetters):
    orientations = ['H', 'V']
    domain = []
    temp = []
    for y in range(0,9):
        for x in range(0, 9):
            for orien in orientations:
                if [y, x, start_letter] in startingLetters:
                    pass
                else:
                    temp = [y, x, orien, False]
                    domain.append(temp)
    return domain
      
#Ensure that word domain values can fit in puzzle
def pruneDomain(word):
    matrixMaxY = 9
    matrixMaxX = 9
    removeList = []
    for value in word.domain:
        if value[2] == 'H' and value[1] > matrixMaxX - word.size:
            removeList.append(value)
        elif value[2] == 'V' and value[0] > matrixMaxY - word.size:
            removeList.append(value)
    for value in removeList:
        word.domain.remove(value)
    return word.domain

#Insert word into puzzle
def insertWord(puzzle, word, value):
    if value[2] == 'H':
        insertx = value[1]
        inserty = value[0]
        for char in word:
            puzzle[inserty][insertx] = char
            insertx += 1

    if value[2] == 'V':
        insertx = value[1]
        inserty = value[0]
        for char in word:
            puzzle[inserty][insertx] = char
            inserty += 1
    return puzzle

#Find the next non-placed variable to assign value to
#Prioritize on whether word has fewer than 4 values left in domain
#or if not, chose the word with the longest word size
def getNextVariable(words):
    words.sort(key= lambda x: x.size, reverse=True)
    maxLength = 0
    longestWord = None
    #Words are sorted in descending order of length
    for word in words:
        if word.placed == False:
            if len(word.domain) == 1:
                longestWord = word
                maxLength = word.size
                break
            if word.placed == True:
                continue
            if word.skip == True:
                word.skip = False
                continue
            if len(word.domain) < 5:
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
    if longestWord == None:
        return False
    else:
        return (longestWord, words.index(longestWord))

#Given word and possible word starting point,
#check whether location is valid and if the word
#results in illegal duplicates in rows, columns, and 3x3 boxes
def doesWordFit(puzzle, word, domain):
    char_index = 0
    if domain[2] == 'H':
        for x in range(domain[1], domain[1]+word.size): 
            #Check the location where each character will be put
            if puzzle[domain[0]][x] != '_' and puzzle[domain[0]][x] != word.word[char_index]:
                return False           
            #Make sure that in row, letter doesn't already exist
            for x_temp in range(0,9):
                if puzzle[domain[0]][x_temp] == word.word[char_index] and x_temp != domain[1]+char_index:
                    return False
            #Make sure that in column, letter doesn't already exist
            for y in range(0,9):
                if  puzzle[y][x] == word.word[char_index] and y != domain[0]:
                    return False
            char_index += 1
        #Check 3x3 box that each char in the word is in
        charx = domain[1]
        chary = domain[0]
        for char in word.word:
            for x in range(charx - charx%3, charx - charx%3 + 3):
                for y in range(chary - chary%3, chary - chary%3 + 3):
                    if puzzle[y][x] == char and x != domain[1]+charx and y != domain[0]:
                        return False
            charx += 1

    elif domain[2] == 'V':
        for y in range(domain[0], domain[0]+word.size): 
            #Check the location where each character will be put
            if puzzle[y][domain[1]] != '_' and puzzle[y][domain[1]] != word.word[char_index]: 
                return False            
            #Make sure that in column, letter doesn't already exist
            for y_temp in range(0,9):
                if  puzzle[y_temp][domain[1]] == word.word[char_index] and y_temp != domain[0]+char_index:
                    return False
            #Make sure that in row, letter doesn't already exist
            for x in range(0,9):
                if puzzle[y][x] == word.word[char_index] and x != domain[1]:
                    return False
            char_index += 1
        #Check 3x3 box that each char in the word is in
        charx = domain[1]
        chary = domain[0]
        for char in word.word:
            for x in range(charx - charx%3, charx - charx%3 +3):
                for y in range(chary - chary%3, chary - chary%3 +3):
                    if puzzle[y][x] == char and y != domain[0]+chary and charx != domain[1]:
                        return False
            chary += 1
    return True

def countValidDomainValues(word):
    count  = 0
    for i in range(0, len(word.domain)):
        if word.domain[i][3] == False:
            count += 1
    return count

def findWordFit(puzzle, word):
    index = 0
    for value in word.domain:
        if value[3] == False:
            if doesWordFit(puzzle, word, value) == True:
                return (value, index)
        index += 1
    return False

def printSudoku(puzzle):
    for y in range(0, 9):
        for x in range(0, 9):
            print(puzzle[y][x], end=" ")
        print()

def printDomain(word):
    i = 0;
    print('start of domain')
    for value in word.domain:
        print (value, end= " ")
        if(i%4 == 0):
            print()
        i += 1
    print()
    print('end of domain')
    print()

def printWords(words):
    for i in range(0,len(words)):
        if (i%4 == 0 and i != 0):
            print()
        print(words[i].word+"\t", end=" ")
    print()
init()