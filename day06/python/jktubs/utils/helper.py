import re
import logging
import math
import sys

# By default the root logger is set to WARNING and all loggers you define
# inherit that value. Here we set the root logger to NOTSET. This logging
# level is automatically inherited by all existing and new sub-loggers
# that do not set a less verbose level.
logging.basicConfig(level=logging.NOTSET)  # https://docs.python.org/3/library/logging.html#levels
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# CRITICAL 50
# ERROR    40
# WARNING  30
# INFO     20
# DEBUG    10
# NOTSET    0
# log.info('info message')
# log.critical('critical message')
# log.debug('debug message')
# log.warning('warning message')
# log.error('error message')

def getVersion():
    log.debug("AoC2020_Day6!")


def read_file_to_list(filename):
    list = []
    file = open(filename, "r")
    for line in file:
        list.append(line)
    file.close()
    return list


# Split string into characters
def split(word):
    return [char for char in word]

# part 1
def get_unique_group_answers(input):
    group_content = [""]
    group_counter = 0
    for i in range(0, len(input)):
        if input[i] != '\n':
            group_content[group_counter] += input[i].strip("\n")
        else:
            group_content[group_counter] = ''.join(set(group_content[group_counter]))  # remove duplicates
            group_counter += 1  # prepare next group
            group_content.append("")

    group_content[group_counter] = ''.join(set(group_content[group_counter]))  # remove duplicates of last entry
    return group_content


# part 2
def get_intersection_group_answers(input):
    group_content_intersection = [""]
    group_counter = 0
    for i in range(0, len(input)):
        if i == 0:
            group_content_intersection[0] = input[i].strip("\n")
        if input[i] != '\n':
            set1 = set(split(group_content_intersection[group_counter]))
            set2 = set(split(input[i].strip("\n")))
            intersection = set1.intersection(set2)
            if intersection:
                group_content_intersection[group_counter] = ''.join(intersection)
            else:
                group_content_intersection[group_counter] = ''
        else:
            group_counter += 1  # prepare next group
            if i < len(input) - 1:
                group_content_intersection.append(input[i + 1].strip("\n"))

    return group_content_intersection
