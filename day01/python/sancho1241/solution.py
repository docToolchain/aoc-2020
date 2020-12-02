def parseInput (puzzleInput):
    myFile = open(puzzleInput, 'r') 
    myList = myFile.read().splitlines() 
    #cast each list item to int
    myIntList = [int(item) for item in myList]
    return myIntList

def solvePuzzle (data):
    result1Found = False
    result2Found = False  
    for num1 in data:
        for num2 in data:
            if not result1Found and (num1 + num2 == 2020):
                print ("Star1:")
                print ("{} plus {} equals {}".format(num1,num2,num1+num2))
                print ("{} times {} equals {}".format(num1,num2,num1*num2))
                result1Found = True
            for num3 in data:
                if not result2Found and (num1 + num2 + num3 == 2020):
                    print ("Star2:")
                    print ("{} plus {} plus {}  equals {}".format(num1,num2,num3,num1+num2+num3))
                    print ("{} times {} times {} equals {}".format(num1,num2,num3,num1*num2*num3))
                    result2Found = True                    
    return

myData = parseInput('input.txt')
solvePuzzle (myData) 