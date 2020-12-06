
import copy

def read_file_to_list(filename):
    """Read file to List"""
    list = []
    person = []
    file = open(filename, "r")
    for line in file:
        if line.strip() == '':
            list.append(person)
            person = []
        else:
            person.append(set([x for x in line.strip()]))
    if person:
        list.append(person)
    file.close()
    return list





def toSet(group):

    head, *tail = copy.deepcopy(group)
    for person in tail:
        head.update(person)
    return head

def toSet2(group):
    head, *tail = copy.deepcopy(group)
    for person in tail:
        head.intersection_update(person)
    return head

#6590
#3288