#!/usr/bin/env python3
from src.util import *
import copy

# tag::starOne[]
data = read_file_to_list("input.txt")

preamble = 25
nc = NumberCache(preamble)

 
for i in range(len(data)):

    if i >= preamble:
        if not nc.valid(data[i]):
            ivn = data[i]
    nc.add(data[i])

print(ivn)

# end::starOne[]



# tag::starTwo[]
nbrs = []

ix = 0
while ix < len(data):
    s = sum(nbrs)
    if s == ivn:
        print(min(nbrs) + max(nbrs))
        break
    if s < ivn:
        nbrs.append(data[ix])
        ix += 1
    if s > ivn:
        nbrs.pop(0)

# end::starTwo[]
