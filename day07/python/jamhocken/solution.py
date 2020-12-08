import re

def process_input(file_contents):      
    container = dict()
    for lines in file_contents:
        regex_outer_bag = re.compile('((\S+\s){2}(bags))\s(contain)')
        outside_bag_tuple = re.findall(regex_outer_bag,lines)
        outside_bag = outside_bag_tuple[0][0].replace(' bags','')

        regex_inner_bag = re.compile('(\d+)\s((\S+\s){2})')
        inside_bag_tuple = re.findall(regex_inner_bag,lines)
        
        temp_list = list()
        for bags in inside_bag_tuple:
            bags_stripped = bags[1].rstrip()
            temp_list.append((bags_stripped,int(bags[0])))
        container.update({outside_bag : temp_list})
    return container

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if graph[start] == []:
        return None
    for node in graph[start]:
        newpath = find_path(graph, node[0], end, path)
        if newpath: return newpath
    return None

def count_bags(dictionary, bag, count_temp):
    count = count_temp
    for outer_bag, inner_bags in dictionary.items():
        if (outer_bag == bag):
            for color, amount in inner_bags:
                count += count_bags(dictionary, color, count_temp*amount)
    return count

with open("bag_rules.txt",'r') as bag_rules: 
    file_contents = bag_rules.readlines()

bag_container = process_input(file_contents)

count = 0
for bags in bag_container:
    if bags != 'shiny gold' and find_path(bag_container, bags, 'shiny gold'):
        count += 1

print(count, 'bag colors can eventually contain at least one shiny gold bag.')

print('My shiny gold bag contains', \
      count_bags(bag_container, 'shiny gold', 1)-1, 'bags.')
      