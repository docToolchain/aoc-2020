#!/usr/bin/env python3
from src.util import *


# tag::starOne[]

schedule = Schedule();
schedule.loadFromFile("input.txt")

depart = schedule.getNextDepartment()

print((depart["time"] -  schedule.arival)* depart["bus"])

# end::starOne[]


# tag::starTwo[]

last = t = 100000000000000
step = 1




candidate = 0
while True:

    t += step

    if(t % 41 != 0):
        continue;
    if((t + 35) % 37 != 0):
        continue;
    if((t + 41) % 911 != 0):
        continue;

    if(candidate == (t - last)):
        step = candidate
        break;
    candidate = t -last
    last = t


candidate = 0
while True:

    t += step

    if((t + 54) % 13 != 0):
        continue;
    if((t + 55) % 17 != 0):
        continue;
    if((t + 64) % 23 != 0):
        continue;
    
    if(candidate == (t - last)):
        step = candidate
        break;
    candidate = t -last
    last = t

while True:

    t += step

    if((t + 70) % 29 != 0):
        continue;
  
    if((t + 72) % 827 != 0):
        continue;
    if((t + 91) % 19 != 0):
        continue;

    print(t)
    break

# end::starTwo[]
