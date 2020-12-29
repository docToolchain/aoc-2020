#!/usr/bin/env python3
from src.util import *

tiles = read_file_to_list("input.txt")

#optimazation, create variants once
for tile in tiles:
    tile.createVariants()

solution = find_solution(tiles,[],set(),0,0)

print(solution[0][0].id * solution[0][-1].id * solution[-1][0].id * solution[-1][-1].id)


# end::starOne[]




# tag::starTwo[]
monster = []
monster.append("                  # ")
monster.append("#    ##    ##    ###")
monster.append(" #  #  #  #  #  #   ")

map = concat_Tiles(solution)
map.createVariants()

for m in map.getVariants():
    r = find_pattern(m,monster)
    if len(r) == 0: continue
    print(m.count() - len(r) * 15)

# end::starTwo[]
