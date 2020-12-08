
import re
import copy

def read_file_to_list(filename):
    """Read file to List"""
    definitions = {}

    list = []
    file = open(filename, "r")
    for line in file:
            m = re.search(r'^([a-z]+)\s+([+-])([0-9]+)', line)
            if not m:
                raise Exception(line)
            cmd = m.group(1).strip();
            sgn = m.group(2).strip();
            arg = int(m.group(3).strip());
            if sgn == '-':
                arg = arg * -1
            
            list.append({ "cmd": cmd , "arg" : arg })

    file.close()
    return list



def process(data):
    indexes = set()
    ix = 0
    acc = 0
    while True:
        if ix in indexes:
            return (False , acc)
        if ix >= len(data):
            return (True , acc)
        indexes.add(ix)
        if data[ix]['cmd'] == "acc":
            acc += data[ix]['arg']
            ix = ix+ 1
        else:
            if data[ix]['cmd'] == "nop":
                ix = ix + 1
            else:
                if data[ix]['cmd'] == "jmp":
                    ix = ix + data[ix]['arg']
    raise Exception("Unreachable")

def fix_command(data,ix):
    data1 = copy.deepcopy(data)
    if(data1[ix]['cmd'] == 'jmp'):
            data1[ix]['cmd'] = 'nop'
    else:
        if(data1[ix]['cmd'] == 'nop'):
            data1[ix]['cmd'] = 'jmp'
    return data1