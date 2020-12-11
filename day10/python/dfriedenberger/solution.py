#!/usr/bin/env python3
from src.util import *
import copy

# tag::starOne[]
data = read_file_to_list("input.txt")
data.sort()

last = 0
d1 = 0
d3 = 1

for e in data:
    diff = e - last
    last = e

    if diff == 1:
        d1 += 1
        continue
    if diff == 3:
        d3 += 1
        continue
    raise Exception("Unknown diff",diff,e)
print(d1*d3)
# end::starOne[]


# tag::possibilities[]
def calc_possibilities(list):
    return [0,1,1,2,4,7][len(list)]
# end::possibilities[]

# tag::starTwo[]




last = 0
l = [0]
f = 1
for e in data:
    diff = e - last
    last = e

    if diff == 1:
        l.append(e)
        continue
    if diff == 3:
        f *= calc_possibilities(l)
        l = [e]
        continue
    raise Exception("Unknown diff",diff,e)

f *= calc_possibilities(l)


print(f)
# end::starTwo[]
