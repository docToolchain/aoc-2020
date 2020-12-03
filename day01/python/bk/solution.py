#!/usr/bin/env python3

# tag::starOne[]
def searchAnswer(Lines, startFromLine, searchedAmount):
    currentLine = startFromLine
    found = False
    secondSummand=int(Lines[startFromLine])
    while currentLine < len(Lines)+1:
        firstSummand = int(Lines[currentLine-1])
        currentAmount = firstSummand + secondSummand
        if currentAmount == searchedAmount:
            found = True
            break
        currentLine+=1

    if(found!=True):
        return searchAnswer(Lines, startFromLine+1, searchedAmount)
    else:        
        return firstSummand*secondSummand
    
f = open("input.txt", "r")
Lines = f.readlines()
answer = searchAnswer(Lines, 1,2020)
print("Answer 1: {}".format(answer))
# end::starOne[]

# tag::starTwo[]
def searchAnswer2(Lines, searchedAmount):
    firstIndex = 0
    found=False  
    while firstIndex < len(Lines):
        secondIndex=firstIndex+1
        while secondIndex < len(Lines):
            thirdIndex=secondIndex+1
            while thirdIndex < len(Lines):
                currentAmount = int(Lines[firstIndex]) + int(Lines[secondIndex]) + int(Lines[thirdIndex])     
                if currentAmount == searchedAmount:
                    found = True
                    break
                thirdIndex+=1
            if found:
                break
            secondIndex+=1
        if found:
            break
        firstIndex+=1

    result = 0
    if found:
        #print("{}+{}+{}={}".format(Lines[firstIndex], Lines[secondIndex], Lines[thirdIndex], currentAmount))
        result = int(Lines[firstIndex]) * int(Lines[secondIndex]) * int(Lines[thirdIndex])
    return result

f = open("input.txt", "r")
Lines = f.readlines()
answer = searchAnswer2(Lines, 2020)
print("Answer 2: {}".format(answer))
# end::starTwo[]
   