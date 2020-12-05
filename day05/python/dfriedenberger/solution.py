#!/usr/bin/env python3
from src.util import *

# tag::starOne[]
data = read_file_to_list("input.txt")

result = []
for seat in data:
    result.append(get_int(seat))
   

print(max(result))

# end::starOne[]
last = 0
for nr in sorted(result):
    if nr != last + 1 and last:
        print(last + 1)
    last = nr

# tag::starTwo[]


# end::starTwo[]
