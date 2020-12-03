#!/usr/bin/env python3
from src.util import *

# tag::starOne[]
passwords = read_file_to_list("input.txt")
result = 0
for (rf,rt,ch,pw) in passwords:
    c = count(pw,ch)
    if(rf <= c and c <= rt):
        result = result + 1;

print(result)

# end::starOne[]


# tag::starTwo[]
passwords = read_file_to_list("input.txt")
result = 0
for (rf,rt,ch,pw) in passwords:
    c = check(pw,rf,ch) + check(pw,rt,ch)
    if(c == 1):
        result = result + 1;
print(result)

# end::starTwo[]
