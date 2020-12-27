#!/usr/bin/env python3
from src.util import *

# tag::starOne[]




p1 , p2  = read_file_to_list("input.txt")

p = play(p1,p2)

print(count(p))

# end::starOne[]

# tag::starTwo[]
p1 , p2  = read_file_to_list("input.txt")

p, _ = play_recursive(p1,p2,0)

print(count(p))

# end::starTwo[]
