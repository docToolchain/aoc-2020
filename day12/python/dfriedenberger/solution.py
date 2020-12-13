#!/usr/bin/env python3
from src.util import *



# tag::starOne[]
commands = read_file_to_list("input.txt")
ship = Ship();

for command in commands:
    ship.process(command)

print(ship.manhattan()) 

# end::starOne[]


# tag::starTwo[]

ship = ShipV2();
for command in commands:
    ship.process(command)

print(ship.manhattan()) 

# end::starTwo[]
