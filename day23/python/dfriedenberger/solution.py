#!/usr/bin/env python3
from src.util import *

# tag::starOne[]


#init = [3,8,9,1,2,5,4,6,7]
init = [4,8,7,9,1,2,3,6,5]
l = len(init)

cups = dict()
for i in range(l):
    cups[init[i]] = init[(i+1) % l]

play(cups,init[0],100)

n = 1
s = ""
for _ in range(l-1):
    s += str(cups[n])
    n = cups[n]

print(s)



# end::starOne[]

# tag::starTwo[]

init = [4,8,7,9,1,2,3,6,5] + list(range(10, 1000001))
l = len(init)

cups = dict()
for i in range(l):
    cups[init[i]] = init[(i+1) % l]

play(cups,init[0],10000000)


p1 = cups[1]
p2 = cups[p1]

print(p1 * p2)

# end::starTwo[]
