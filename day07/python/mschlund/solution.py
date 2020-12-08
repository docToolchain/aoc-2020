import networkx as nx
import re

def add_edges(line, G):
  color = '[a-z]+ [a-z]+'
  container = '([0-9]) (' + color + ') bags?'
  node_pattern = re.compile('(' + color + ') bags contain (.*)')
  m = re.match(node_pattern, line)
  node = m.group(1)
  rest = m.group(2)
  contents = rest.split(',')
  for c in contents:
    dest_match = re.match(container, c.strip(' .'))
    if dest_match:
      dest_weight = int(dest_match.group(1))
      dest_node = dest_match.group(2)
      G.add_edge(node, dest_node, weight=dest_weight)

def get_total_weight(G, s):
  if G.out_degree(s) == 0:
    return 0
  neighbors = G.successors(s)
  weight_of_neighbors = [(get_total_weight(G, v) + 1) * G[s][v]['weight'] for v in G.successors(s)]
  return sum(weight_of_neighbors)

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    G = nx.DiGraph()
    for line in input:
      add_edges(line, G)
    
    # star 1:
    transitive_closure = nx.transitive_closure(G)
    num_pred = len(list(transitive_closure.predecessors('shiny gold')))
    print('We have {} predecessors of "shiny gold"'.format(num_pred))

    #star 2:
    needed_bags = get_total_weight(G, 'shiny gold')
    print('The shiny gold bag contains {} bags.'.format(needed_bags))

if __name__ == "__main__":
  main()
