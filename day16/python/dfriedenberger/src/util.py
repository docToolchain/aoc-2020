import re
import numpy as np


def read_file_to_list(filename):
        """Read file to map"""
        fields = {}
        tickets = []
        file = open(filename, "r")
        for line in file:
            if line.strip() == "": continue
            if line.strip() == "your ticket:": continue
            if line.strip() == "nearby tickets:": continue
            
            #seat: 13-40 or 45-50
            m = re.search(r'^([a-z\s]+):\s+([0-9]+)[-]([0-9]+)\s+or\s+([0-9]+)[-]([0-9]+)$', line)
            if m: 
                fields[m.group(1)] = [
                    {"from" : int(m.group(2)), "to" : int(m.group(3))},
                    {"from" : int(m.group(4)), "to" : int(m.group(5))}
                ]
                continue
            #7,1,14
            m = re.search(r'^([0-9,]+)', line)
            if m: 
                tickets.append([int(x) for x in m.group(1).split(',')])
                continue
            raise Exception(line)
        return fields , tickets

def scanning(fields , tickets):
    invalid = []
    position = {}
    for ticket in tickets:
        valid = True
        lposition = {}
        for i in range(len(ticket)):
            nr = ticket[i]
            match = set()
            for key, ranges in fields.items():
                for r in ranges:
                    if r["from"] <= nr and nr <= r["to"]:
                        match.add(key)
            lposition[i] = match
            if len(match) == 0:
                invalid.append(nr)
                valid = False
        if valid:
            #merge
            for key, value in lposition.items():
                if not key in position:
                    position[key] = lposition[key]
                else:
                    position[key].intersection_update(lposition[key])
    #print(position)

    solved = set()
    while True:
        single = None
        for key, values in position.items():
            if len(values) == 1:
                single = next(iter(values))
                if single in solved: single = None
                else: break
        if single == None: break
        for key, values in position.items():
            if len(values) > 1:
                if single in position[key]:
                    position[key].remove(single)
        solved.add(single)


    return sum(invalid)  , position

