#!/usr/bin/env python3
from src.util import *



# tag::starOne[]
lines = read_file_to_list('input.txt')

sum = 0
for line in lines:
    sum += solve(line)
print(sum)

# end::starOne[]


# tag::starTwo[]
sum = 0
for line in lines:
    sum += solve2(line)
print(sum)
# end::starTwo[]
