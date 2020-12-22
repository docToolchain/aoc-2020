import re
import numpy as np


def read_file_to_list(filename):
        """Read file to map"""
        lines = []
        file = open(filename, "r")
        for line in file:
            if line.strip() == "": continue
            lines.append(line)
        return lines

def solve(line):
    #solve ()
    while True:
        m = re.search(r'[(]([0-9\s+*]+)[)]', line)
        if not m: break;
        val = solve(m.group(1))
        line = line[:m.start()] + str(val) + line[m.end():]
    
    while True:
        # tag::substring[]
        m = re.search(r'([0-9]+)\s+([+*])\s+([0-9]+)', line)
        # end::substring[]
        if not m: break;
        val1 = int(m.group(1))
        op = m.group(2)
        val2 = int(m.group(3))
        if op == "*":
            val = val1 * val2
        else: 
            if op == "+":
                val = val1 + val2
            else : raise Exception(op)
        # tag::substring[]
        line = line[:m.start()] + str(val) + line[m.end():]
        # end::substring[]
    return int(line)

def solve2(line):

    while True:
        m = re.search(r'[(]([0-9\s+*]+)[)]', line)
        if not m: break;
        val = solve2(m.group(1))
        line = line[:m.start()] + str(val) + line[m.end():]
    
    while True:
        m = re.search(r'([0-9]+)\s+[+]\s+([0-9]+)', line)
        if not m: break;
        val1 = int(m.group(1))
        val2 = int(m.group(2))
        val = val1 + val2
        line = line[:m.start()] + str(val) + line[m.end():]

    while True:
        m = re.search(r'([0-9]+)\s+[*]\s+([0-9]+)', line)
        if not m: break;
        val1 = int(m.group(1))
        val2 = int(m.group(2))
        val = val1 * val2
        line = line[:m.start()] + str(val) + line[m.end():]

    return int(line)





