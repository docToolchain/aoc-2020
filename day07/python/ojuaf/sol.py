import doctest
import logging
import math as m
import re
from networkx import DiGraph


def load_input():
    answers = set()
    pattern = re.compile("(\w+) (\w+) bags contain (.+)")
    grph = DiGraph()
    with open('input.txt') as fd:
        for line in fd:
            match = pattern.search(line.strip())
            source_bag = "{0} {1}".format(match.group(1), match.group(2))
            dests = match.group(3)
            dests = dests.split(',')
            dests = list(map(lambda x: x.strip(), dests))
            for dest in dests:
                spl_dest = dest.split()
                if spl_dest[0].isnumeric():
                    number = int(dest[0])
                    dest_bag = "{0} {1}".format(spl_dest[1], spl_dest[2])
                    grph.add_edge(source_bag, dest_bag, number=number)
    return grph


def predecessors(grph, node):
    result = set()
    for node in grph.predecessors(node):
        result.add(node)
        result = result.union(predecessors(grph, node))
    return result


def successors(grph, node):
    result = 1
    for pdnode in grph.successors(node):
        number = grph.edges[node, pdnode]['number']
        result += number * successors(grph, pdnode)
    return result


def main():
    grph = load_input()
    nodes = []
    result = predecessors(grph, "shiny gold")
    print("Part1: %d" % len(result))

    result = successors(grph, "shiny gold")
    # Subtract shiny gold bag
    print("Part2: %d" % (result - 1))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
