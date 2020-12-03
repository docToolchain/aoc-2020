#!/usr/bin/env python3
from src.example import *

# tag::starOne[]
numbers = read_file_to_list("input.txt")
currentFrequency = 0
for number in numbers:
    currentFrequency += number
print("Solution Star One: ", currentFrequency)
# end::starOne[]


# tag::starTwo[]

example = Example("Test")

print("My name is", example.name)
print("My name is", example.get_name())


# end::starTwo[]
