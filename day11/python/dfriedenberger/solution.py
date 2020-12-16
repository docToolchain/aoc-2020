#!/usr/bin/env python3
from src.util import *


# tag::starOne[]

seatMap = SeatMap()
seatMap.loadFromFile("input.txt")

cnt = 0
run = True
while run:
    seatMapNext = seatMap.next()
    cnt += 1
    if seatMapNext.equals(seatMap): run = False
    seatMap = seatMapNext

print(seatMap.count()) 

# end::starOne[]


# tag::starTwo[]

seatMap = SeatMap()
seatMap.loadFromFile("input.txt")

cnt = 0
run = True
while run:
    seatMapNext = seatMap.next2()
    cnt += 1
    if seatMapNext.equals(seatMap): run = False
    seatMap = seatMapNext

print(seatMap.count())    

# end::starTwo[]
