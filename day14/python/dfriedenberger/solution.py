#!/usr/bin/env python3
from src.util import *



# tag::starOne[]
commands = read_file_to_list("input.txt")

mem = {}
for command in commands:
    if(command['type'] == 'mask'):
        mask = command['mask']
        continue;
    if(command['type'] == 'mem'):
        mem[command['address']] = process(mask,command['value'])

print(sum(mem.values()))

# end::starOne[]


# tag::starTwo[]

mem = {}
for command in commands:
    if(command['type'] == 'mask'):
        mask = command['mask']
        continue;
    if(command['type'] == 'mem'):
        addresses = process_address(mask,command['address'])
        for address in addresses:
            mem[address] = command['value']

print(sum(mem.values()))
# end::starTwo[]
