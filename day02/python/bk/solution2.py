#!/usr/bin/env python3
class Policy:
    def __init__(self, lowestNumber, highestNumber, letter):
        self.lowestNumber = lowestNumber
        self.highestNumber = highestNumber
        self.letter = letter

class ParsedEntry:
    def __init__(self, entryAsString):
        self.policy = self.__parsePolicy(entryAsString)
        self.password = self.__parsePassword(entryAsString)
        #print("{}-{} {}: {}".format(self.policy.lowestNumber, self.policy.highestNumber, self.policy.letter, self.password))
    def __parsePolicy(self, entryAsString):
        pos1 = entryAsString.find('-')
        lowestNumber = int(entryAsString[:pos1])
        pos2 = entryAsString.find(' ')
        highestNumber = int(entryAsString[pos1+1:pos2+1])
        letter = entryAsString[pos2+1:pos2+2]
        p = Policy(lowestNumber, highestNumber, letter)
        return p
    def __parsePassword(self, entryAsString):
        pos = entryAsString.find(':')
        password = entryAsString[pos+2:]
        return password

class Validtor:
    def __init__(self, entries):
        self.entries = entries
        self.numberOfValidPasswords = 0
    def validate(self):
        currentLine = 1
        for e in entries:
            pE = ParsedEntry(e)
            isValid = self.__validatePassword(pE.policy, pE.password)
            #print("{}:{}-{} {}: {} = {}".format(currentLine, pE.policy.lowestNumber, pE.policy.highestNumber, pE.policy.letter, pE.password, isValid))
            if isValid:
                self.numberOfValidPasswords+=1
            currentLine+=1
    def __validatePassword(self, policy, password):
        containsOnFirstPosition = password[policy.lowestNumber-1] == policy.letter
        containsOnSecondPosition = password[policy.highestNumber-1] == policy.letter
        if(containsOnFirstPosition == True and containsOnSecondPosition == True):
            return False
        if(containsOnFirstPosition == False and containsOnSecondPosition == False):
            return False
        return True

f = open("input.txt", "r")
entries = f.readlines()
v = Validtor(entries)
v.validate()
print(v.numberOfValidPasswords)