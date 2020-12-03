def parseInput (puzzleInput):
    # read password lines
    myFile = open(puzzleInput, 'r') 
    myList = myFile.read().splitlines() 
    
    #remove unnecessary chars, split contents and cast numbers to int
    for pos, value in enumerate(myList):
        myList[pos] = value.replace("-"," ").replace(":","").split()
        myList[pos][0] = int(myList[pos][0])
        myList[pos][1] = int(myList[pos][1])       
    
    return myList

def solvePuzzlePart1 (passwords):
    validPasswordsCounts = 0  
    for line in passwords:
        # check if char occurence in password is between upper and lower limit
        if (line[0] <= line[3].count(line[2]) <= line[1]):
            validPasswordsCounts += 1
    return "Star1: " + str(validPasswordsCounts) + " valid passwords"

def solvePuzzlePart2 (passwords):
    validPasswordsCounts = 0  
    for line in passwords:
        if (line[3][line[0]-1] == line[2]) != (line[3][line[1]-1] == line[2]):  
            validPasswordsCounts += 1   
    return "Star2: " + str(validPasswordsCounts) + " valid passwords"

passwordList = parseInput('input.txt')

print(solvePuzzlePart1(passwordList)) 
print(solvePuzzlePart2(passwordList)) 