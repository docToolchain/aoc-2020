#!/usr/bin/env python3
from src.util import *

# tag::starOne[]
numbers = read_file_to_list("input.txt")
result = set()
for number1 in numbers:
    for number2 in numbers:
        if(number1 + number2 == 2020):
            #print(number1, number2)
            result.add(number1 * number2)

print(result)
# end::starOne[]


# tag::starTwo[]
numbers = read_file_to_list("input.txt")
result = set()
for number1 in numbers:
    for number2 in numbers:
        for number3 in numbers:
            if(number1 + number2 + number3 == 2020):
                #print(number1, number2, number3)
                result.add(number1 * number2 * number3)
print(result)

# end::starTwo[]
