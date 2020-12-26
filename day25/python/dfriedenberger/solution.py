#!/usr/bin/env python3
from src.util import *

# tag::starOne[]


def enckey(subject,loop):
    value = 1
    for i in range(loop):
        value = value * subject
        value = value % 20201227
    return value




#p1 = 5764801
#p2 = 17807724
p1 = 17607508
p2 = 15065270

subject = 7
value = 1
loop = 0
loop1 = None
loop2 = None
while not loop1 and not loop2:
    value = value * subject
    value = value % 20201227
    loop += 1
    if value == p1: loop1 = loop
    if value == p2: loop2 = loop

#print(loop1,loop2)
if loop2: print(enckey(p1,loop2))
if loop1: print(enckey(p2,loop1))

# end::starOne[]

# tag::starTwo[]


# end::starTwo[]
