import draw_hangman as d

gl_word = ''
misses = 0
charCorrect = []
charWrong = []
isWin = False
print('1',gl_word)

def gameGuess(word):
    global gl_word, misses, isWin
    gl_word = word
    print('2',gl_word)
    charInput = askPlayerInput()
    if charInput in word:
        charCorrect.append(charInput)
        print(charInput)
    else:
        charWrong.append(charInput)
        misses+=1
    showCorrectAndWrongGuess(word)
    d.draw(misses,charWrong)
    isWin = checkWin(charCorrect, word)

def checkWin(correct,word):
    global isWin
    #if list(word) in charCorrect:
    #    isWin = True
    if all(char in correct or char == ' ' for char in word):
        isWin = True
        print('You win!')
        return True
    return False

def askPlayerInput():
    validInput = False
    while validInput == False:
        charInput = input('\nEnter a single character: ')
        if charInput in charCorrect or charInput in charWrong:
            print('Please enter other char')
        elif charInput.isalpha() and charInput!=' ' and len(charInput)==1:
            validInput = True
        else:
            print('Please enter only one character!')
    return charInput

def showCorrectAndWrongGuess(word):
    wordSplit = list(word)
    print('Word:')
    for i, char in enumerate(word):
        if char == ' ':
            print(' ', end="")
        elif char in charCorrect:
            print(char, end="")
        else:
            print('_', end="")

while misses<7 and not isWin:
    gameGuess(gl_word)