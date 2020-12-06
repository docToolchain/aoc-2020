#!/usr/bin/env python3
from src.util import *

# tag::starOne[]
data = read_file_to_list("input.txt")

result = 0
for d in data:
    s = toSet(d)
    result = result + len(s)

print(result)

# end::starOne[]


# tag::starTwo[]

result = 0
for d in data:
    s = toSet2(d)
    result = result + len(s)

print(result)
# end::starTwo[]
