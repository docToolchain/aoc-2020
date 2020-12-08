#!/usr/bin/env python3
from src.util import *
import copy

# tag::starOne[]
data = read_file_to_list("input.txt")
_, result = process(data)
print(result)
# end::starOne[]



# tag::starTwo[]
for ix in range(len(data)):
    data1 = fix_command(data,ix)
    terminate, result = process(data1)
    if terminate:
        print(result)
        break;

    
# end::starTwo[]
