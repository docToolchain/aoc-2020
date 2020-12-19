#!/usr/bin/env python3
from src.util import *


# tag::starOne[]
cube = Cube()
cube.loadFromFile("input.txt")

for i in range(0,6):
    cube = cube.next()

print(cube.count())

# end::starOne[]


# tag::starTwo[]
cube = Cube4D()
cube.loadFromFile("input.txt")
for i in range(0,6):
    cube = cube.next()

print(cube.count())
# end::starTwo[]
