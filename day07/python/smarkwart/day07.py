import sys
import re

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        data_list = input_file.readlines()
    return data_list

def prepare_data(input_data):
    """
    parse the data into a dictionary
    """
    the_data = []
    for line in input_data:
        splitted_line = line.split(' bags contain ')
        new_bag = {'color':splitted_line[0]}
        new_bag['children'] = []
        children = re.split(r" bag[s,. ]*", splitted_line[1].strip())
        for child in children:
            if child != "":
                regex_match = re.match(r"(?P<count>\d) (?P<color>\w* \w*)",child)
                if regex_match:
                    dataset = regex_match.groupdict()
                    new_bag['children'].append(dataset)
        the_data.append(new_bag)
    return the_data

def print_data(the_rules):
    """
    used this function to visualize the content of the dictionary
    """
    for rule in the_rules:
        print(f"Rule for {rule['color']} bag has the children: ")
        for child in rule['children']:
            print(f"\t{child['count']} bags in {child['color']}")

def gather_possible_containers(the_rules, bag_color="shiny gold"):
    """
    evaluate recursively how many continers can possibly contain a bag_color colored bag
    """
    containers_found = []
    for rule in the_rules:
        for child in rule['children']:
            if child['color'] == bag_color and rule['color'] not in containers_found:
                containers_found.append(rule['color'])
                containers_found.extend(gather_possible_containers(the_rules, rule['color']))
    return containers_found

def count_contained(the_rules, bag_color="shiny gold"):
    """
    count recursively how many bags this bag contains
    """
    count = 0
    for rule in the_rules:
        if rule['color'] == bag_color:
            #count this bag
            count += 1
            for child in rule['children']:
                count_children = count_contained(the_rules, child['color'])
                if count_children != 0:
                    count += int(child['count']) * count_children
                else:
                    count += int(child['count'])
                #print(f"\t{child['count']} bags in {child['color']} which contains {count_children} bags so we have {count}")
    return count

input_data = get_input_data_as_list(sys.argv[1])
the_rules = prepare_data(input_data)

containers_without_duplicates = set(gather_possible_containers(the_rules))

print(f"Star1: The shiny gold bag can be contained in {len(containers_without_duplicates)} bags")

#need to substract -1 because of self is contained in order to get right sum
print(f"Star2: The shiny gold bag can contain {count_contained(the_rules)-1} bags")
