#!/usr/bin/env python3
from src.util import *

# tag::starOne[]
data = read_file_to_list("input.txt")

result = 0
for d in data:
    valid = check_password(d)
    if valid:
        result = result + 1

print(result)

# end::starOne[]


# tag::starTwo[]
result = 0
for d in data:
    valid = check_password2(d)
    if valid:
        result = result + 1

print(result)

# end::starTwo[]
