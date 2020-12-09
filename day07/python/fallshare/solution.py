from pathlib import Path
import networkx as nx
import re

def read_input_file(input_file_path):
    p = Path(input_file_path)

    G = nx.DiGraph()

    with p.open() as input_file: 
        for line in input_file:
            #remove newlines, final dot and split into soruce and target parts
            source, targets = line.strip().strip(".").split(" contain ")

            #removing trailing s from bags to unify bag descriptions 
            source = source.rstrip("s")
            G.add_node(source)

            targets = targets.split(", ")
            if targets[0] == 'no other bags': 
                targets = None
            else:       
                for target in targets:
                    amount, target_bag = re.match("^(\d+) (.*)$",target).groups()
                    if amount != 1: target_bag = target_bag.rstrip("s")

                    G.add_node(target_bag)

                    G.add_edge(source, target_bag, weight=amount)

    return G

def get_all_parent_bags(graph, start_bag):
    parent_bags = set()
    for bag in graph.predecessors(start_bag):
        parent_bags.add(bag)
       
        #add all parent bag of current bag, using set and update ensures that duplicates are ignored
        parent_bags.update(get_all_parent_bags(graph, bag))
    return parent_bags

def get_all_bags_inside_bag(graph, start_bag):
    bag_count = 1
    
    for bag in graph.successors(start_bag):
        #start_bag -> bag --> weight rausfinden
        weight = int(graph.get_edge_data(start_bag,bag)['weight'])
       
        #add all parent node of current node, using set and update ensures that duplicates are ignored
        bag_count += (weight * get_all_bags_inside_bag(graph, bag))
        
    if bag_count == 0:
        bag_count = 1

    return bag_count

if __name__ == "__main__":
    graph = read_input_file("input.txt")
    
    shiny_golden_bag_colors = len(get_all_parent_bags(graph, 'shiny gold bag'))
    print(f"Star 1: Number of colors for shiny golden bag: {shiny_golden_bag_colors}")
    print(f"Star 2: Number of bags inside shiny golden bag: {get_all_bags_inside_bag(graph, 'shiny gold bag') - 1}")