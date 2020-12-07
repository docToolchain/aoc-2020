
import re

def read_file_to_list(filename):
    """Read file to List"""
    definitions = {}

    file = open(filename, "r")
    for line in file:
            keybag , defbags = line.strip().split('contain')
            rules = defbags.split(',')
            m = re.search("^([a-z\s]+)bag", keybag)
            if not m:
                raise Exception(keybag)
            bag = m.group(1).strip();
            definitions[bag] = []
            for rule in rules:
                if "no other bag" in rule:
                    continue
                m = re.search("([0-9]+)([a-z\s]+)bag", rule)
                if not m:
                    raise Exception(rule)
                nr = int(m.group(1))
                color = m.group(2).strip()
                definitions[bag].append({ "color": color , "nr" : nr })

    file.close()
    return definitions



def hasShinyGold(definitions,key):

    if key == "shiny gold":
        return True

    for rule in definitions[key]:
        if hasShinyGold(definitions,rule["color"]):
            return True
    return False

def countBags(definitions,key):
    result = 1 #bag itself
    for rule in definitions[key]:
        result +=  rule["nr"]  * countBags(definitions,rule["color"])
    return result