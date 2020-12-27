import re
import copy


def read_file_to_list(filename):
        """Read file to map"""
        lists = { "1" : [], "2" : []}
        i = None
        file = open(filename, "r")
        for line in file:
            line = line.strip()
            if line == "": continue

            m = re.search(r'^Player ([12]):$', line)
            if m: 
                i = m.group(1)
                continue
            lists[i].append(int(line))
       
        return lists["1"] , lists["2"]


def play(p1,p2):

    played = set()
    while len(p1) > 0 and len(p2) > 0:
        conf = "{0}#{1}".format(",".join(map(str, p1)),",".join(map(str, p2)))
        if conf in played: 
            return []
        played.add(conf)
        v1 = p1.pop(0)
        v2 = p2.pop(0)
        if v1 > v2:
            p1 += [v1,v2]
        else:
            p2 += [v2,v1]
    if len(p1) > 0:
        return p1
    return p2



def play_recursive(p1,p2,deep):

    played = set()
    while len(p1) > 0 and len(p2) > 0:

        conf = str(p1)+str(p2)
        if conf in played: 
            return [] , "1"
        played.add(conf)



        v1 = p1.pop(0)
        v2 = p2.pop(0)

        win = "0"
        if v1 <= len(p1) and v2 <= len(p2):
            #subgame
            _ , win = play_recursive(copy.deepcopy(p1[:v1]),copy.deepcopy(p2[:v2]),deep+1)
        if win == "0":
            if v1 > v2:
                win = "1"
            else:
                win = "2"

        if win == "1":
            p1 += [v1,v2]
        else:
            p2 += [v2,v1]

            
    result = None
    if len(p1) > 0:
        result = p1 , "1"
    else:
        result = p2 , "2"

    #cache[key] = result
    return result


def count(p):
    sum = 0
    l = len(p)
    for i in range(l):
        sum += p[i] * (l - i)
    return sum