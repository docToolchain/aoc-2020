#!/usr/bin/env python3
from src.util import *

# tag::starOne[]

lines = read_file_to_list("input.txt")
tiles = Tiles()
for line in lines:
    flip_tiles(tiles,line)
print(tiles.countBlack())


# end::starOne[]



# tag::starTwo[]

for d in range(0,100):
    daily_flip_tiles(tiles)
print(tiles.countBlack())

# end::starTwo[]
