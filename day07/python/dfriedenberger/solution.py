#!/usr/bin/env python3
from src.util import *

# tag::starOne[]
result = 0
data = read_file_to_list("input.txt")
for key in data:
    if key == "shiny gold":
        continue #Ignore
    if hasShinyGold(data,key):
        result = result + 1
print(result)

# end::starOne[]


# tag::starTwo[]

result = countBags(data,"shiny gold") - 1
print(result)

# end::starTwo[]
