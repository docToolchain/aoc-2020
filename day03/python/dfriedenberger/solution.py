#!/usr/bin/env python3
from src.util import *

# tag::countTrees[]
def count_trees(treeMap,xsteps,ysteps):
    x = 0
    y = 0
    trees = 0
    while(y < treeMap.height):
        c = treeMap.get(x,y)
        if(c == '#'):
            trees = trees + 1;
        x = (x + xsteps) %  treeMap.width
        y = y + ysteps
    return trees
# end::countTrees[]

# tag::starOne[]

treeMap = TreeMap("input.txt")
trees = count_trees(treeMap,3,1)
print(trees)
# end::starOne[]


# tag::starTwo[]
result = 1
for (x,y) in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
    result = result * count_trees(treeMap,x,y)
print(result)

# end::starTwo[]
