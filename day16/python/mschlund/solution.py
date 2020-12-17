from collections import defaultdict
import math
import networkx as nx
import networkx.algorithms.bipartite

def parse_field_and_ranges(section):
  constraints_string = section.split('\n')
  ranges = {}
  for c in constraints_string:
    field_name = c.split(':')[0]
    ranges[field_name] = []
    ranges_str = c.split(':')[1].split('or')
    for r in ranges_str:
      range_tuple = (int(r.split('-')[0]), int(r.split('-')[1]))
      ranges[field_name].append(range_tuple)
  return ranges

def check_other_tickets(section, ranges):
  lines = section.split('\n')[1:]
  error_rate = 0
  valid_tickets = []
  for line in lines:
    numbers = line.split(',')
    ticket_erroneous = False
    for n in numbers:
      num_int = int(n)
      flattened_vals = [x for l in ranges.values() for x in l]
      res = [m <= num_int and num_int <= M for (m,M) in flattened_vals]
      if not any(res):
        error_rate += num_int
        ticket_erroneous = True
    if not ticket_erroneous:
      valid_tickets.append(line)
  return error_rate, valid_tickets


def get_field_positions(valid_tickets, ranges):
  field_positions = defaultdict(list)
  field_to_pos = {f : set(range(valid_tickets[0].count(',')+1)) for f in ranges.keys()}

  for ticket in valid_tickets:
    numbers = map(int, ticket.split(','))
    for i,n in enumerate(numbers):
      for field_name in ranges.keys():
        (m1, M1), (m2, M2) = ranges[field_name]
        if (m1 <= n and n <= M1) or (m2 <= n and n <= M2):
          field_positions[field_name].append(i)
        else:
          if i in field_to_pos[field_name]:
            #print('{} cannot be {}, {} not in range'.format(i, field_name, n))
            field_to_pos[field_name].remove(i)
  return field_to_pos

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    input_string = input.read()
    input_split = input_string.split('\n\n')
    ranges = parse_field_and_ranges(input_split[0])
    error_rate, valid_tickets = check_other_tickets(input_split[2], ranges)
    # star 1:
    print('Error rate: {}'.format(error_rate))
    # star 2:
    positions = get_field_positions(valid_tickets, ranges)
    G = nx.Graph()
    for f in positions.keys():
      for v in positions[f]:
        G.add_edge(f, v)
    matching = nx.algorithms.bipartite.hopcroft_karp_matching(G)
    departure_indices = [matching[x] for x in matching.keys() if type(x)==str and x.startswith('departure')]
    print(departure_indices)
    my_ticket = [int(x) for x in input_split[1].split('\n')[1].split(',')]
    print('Product of all departure-fields: {}'.format(math.prod([my_ticket[i] for i in departure_indices])))

if __name__ == "__main__":
  main()
