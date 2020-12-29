#!/usr/bin/env python3
from src.util import *



# tag::starOne[]
rules, rows = read_file_to_list("input.txt")



valid = 0
for row in rows:
    if match(rules,row):
          valid += 1

print(valid)
# end::starOne[]


# tag::starTwo[]
rules["8"] = { "type" : "or" , "parts1" : ["42"], "parts2" : ["42", "8"] }
rules["11"] = { "type" : "or" , "parts1" : ["42", "31" ], "parts2" : ["42", "11" ,"31"] }

valid = 0
for row in rows:
    if match(rules,row):
          valid += 1

print(valid)

# end::starTwo[]
