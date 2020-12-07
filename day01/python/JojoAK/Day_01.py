# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 21:56:51 2020

@author: Johannes
"""

#PuzzleInput = PuzzleInput.txt

f = open("PuzzleInput.txt")
txt = f.readlines()

#txt = [1721, 979, 366, 299, 675, 1456]

nr1 = 0
nr2 = 0
nr3 = 0
i=0
k=0
j=0
summe = 0


for i in txt:
    nr1 = int(i)
    for k in txt:
        nr2 = int(k)
        for j in txt:
            nr3 = int(j)
            summe = nr1+nr2+nr3
        
            if summe == 2020:
                result = nr1 * nr2 * nr3
                print(result)
            else:
                summe = 0
        
