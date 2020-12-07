#!/usr/bin/env python3
class TreeCounter:
    def __init__(self, entries, right, down):
        self.entries = entries
        self.right=right
        self.down=down
        self.countedTrees=0
        self.currentLineIndex=0
        self.currentPos=1
        self.lineSize=31
        self.currentLine=""
    def countTrees(self):
        while 1 > 0:   
            self.__stepRight()                     
            self.__stepDown()     
            if self.currentLine == "":
                break;
            currentElement=self.__getElement()
            if currentElement == '#':
                self.countedTrees+=1            
    def __stepDown(self):
        self.currentLineIndex+=self.down
        if self.currentLineIndex >= len(self.entries):
            self.currentLine = ""
            return
        self.currentLine = self.entries[self.currentLineIndex]
    def __stepRight(self):
        self.currentPos+=self.right            
        if self.currentPos >= self.lineSize+1:
            self.currentPos = self.currentPos - self.lineSize        
    def __getElement(self):
        currentElement=self.currentLine[self.currentPos-1]
        return currentElement

f = open("input.txt", "r")
entries = f.readlines()
c = TreeCounter(entries, 3, 1)
c.countTrees()
print("Answer 1: {}".format(c.countedTrees))