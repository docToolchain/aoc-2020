import re
import numpy as np


def read_file_to_list(filename):
        """Read file to map"""
        rows = []
        rules = {}
        file = open(filename, "r")
        for line in file:
            line = line.strip()
            if line == "": continue

            #3: 4 5 6
            m = re.search(r'^([0-9]+):\s+([0-9\s+]+)$', line)
            if m: 
                rules[m.group(1)] = { "type" : "concat" , "parts" : m.group(2).split(" ") }
                continue
            #3: "a"
            m = re.search(r'^([0-9]+):\s+["]([ab])["]$', line)
            if m: 
                rules[m.group(1)] = { "type" : "singlechar" , "char" : m.group(2) }
                continue

            #3: 4 5 | 5 4
            m = re.search(r'^([0-9]+):\s+([0-9\s]+)\s+[|]\s+([0-9\s]+)$', line)
            if m: 
                rules[m.group(1)] = { "type" : "or" , "parts1" : m.group(2).split(" ") , "parts2" : m.group(3).split(" ") }
                continue

            m = re.search(r'^([ab]+)$', line)
            if m: 
                rows.append(m.group(1))
                continue
            raise Exception(line)
        return rules,  rows

# tag::backtracking[]
def match_rule_variants(rules, word, r , ixList):
    p = []
    for ix in ixList:
        p += match_rule(rules, word , r, ix)
    
    return p

def match_rules(rules, word, rl , ix):
    il = [ix]
    for r in rl:
        #Try out each il
        ili = il
        il = match_rule_variants(rules, word , r, il)

        #print("match_rules",rl,"pos",ili,"=>",il)
        if len(il) < 0: return 0

    #print("pos",ix,"match_rules (list)",rl,il)
    return il

def match_rule(rules, word , r, ix):
    #print("pos",ix,"checkrule (start)",r)
    rule = rules[r]
    if(ix >= len(word)): return []

    if rule["type"] == "singlechar":
        #print("check", rule["char"] , word[ix], rule["char"] == word[ix] , word,ix)
        if rule["char"] == word[ix]: return [ix + 1]
        return []
    
    if rule["type"] == "or":
        p = []
        p += match_rules(rules, word ,rule["parts1"], ix )
        p += match_rules(rules, word ,rule["parts2"], ix )
        #print("pos",ix,"match_rule (or) found",p)
        return p

    if rule["type"] == "concat":
        return match_rules(rules, word ,rule["parts"], ix )



def match(rules, word):
    pos = match_rule(rules,word,"0",0)
    for p in pos:
        if p == len(word): return True
    return False
# end::backtracking[]
