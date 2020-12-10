import networkx as nx

def parse_line(i, line, G):
  split_line = line.split(' ')
  instruction = split_line[0]
  if instruction == 'acc':
    dest = i+1
    weight = int(split_line[1])
  elif instruction == 'nop':
    dest = i+1
    weight = 0
  elif instruction == 'jmp':
    dest = i+int(split_line[1])
    weight = 0
  G.add_edge(i, dest, weight=weight)

def get_acc_count(G, s, acc, visited):
  if s in visited:
    visited.remove(s)
    return acc
  elif list(G.successors(s)) == []:
    return acc
  else:
    visited.add(s)
    for v in G.successors(s):
      return get_acc_count(G, v, acc + G.get_edge_data(s,v)['weight'], visited)

def read_graph(input_string):
  all_lines = input_string.split('\n')
  G = nx.DiGraph()
  for i, line in enumerate(all_lines):
    parse_line(i, line, G)
  return G

def switch_statement(i , input_string):
  all_lines = input_string.split('\n')
  line = all_lines[i]
  stmt, num = line.split(' ')[0], line.split(' ')[1]
  if stmt == 'acc':
    return False, input_string
  elif stmt == 'jmp':
    new_line = 'nop {}'.format(num)
  elif stmt == 'nop':
    new_line = 'jmp {}'.format(num)
  return True, '\n'.join(all_lines[:i] + [new_line] + all_lines[i+1:])

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    G = read_graph(input.read())
  acc = get_acc_count(G, s=0, acc=0, visited=set([]))

  print('Star 1 -- acc-count until cycle: {}'.format(acc))

  lines = G.size()
  input = open(input_filename, 'r')
  input_string = input.read()
  for i in range(lines-1):
    b, stream = switch_statement(i, input_string)
    if b:
      G = read_graph(stream)
      try:
        nx.find_cycle(G, source=0)
      except nx.exception.NetworkXNoCycle:
        acc = get_acc_count(G, s=0, acc=0, visited=set([]))
        print('Star 2 -- acc-count for modified cycle-free-program: {}'.format(acc))


if __name__ == "__main__":
  main()