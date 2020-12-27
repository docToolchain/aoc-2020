#!/usr/bin/env python3
from src.util import *



# tag::starOne[]
fields, tickets = read_file_to_list('input.txt')
error_rate, positions = scanning(fields, tickets)
print(error_rate)
# end::starOne[]


# tag::starTwo[]
m = 1
for key,values in positions.items():
    if next(iter(values)).startswith('departure'):
        m *= tickets[0][key]

print(m)
# end::starTwo[]
