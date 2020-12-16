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
    for n in numbers:
      num_int = int(n)
      flattened_vals = [x for l in ranges.values() for x in l]
      res = [m <= num_int and num_int <= M for (m,M) in flattened_vals]
      if not any(res):
        error_rate += num_int
      else:
        valid_tickets.append(line)
  return error_rate, valid_tickets

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    input_string = input.read()
    input_split = input_string.split('\n\n')
    ranges = parse_field_and_ranges(input_split[0])
    error_rate, valid_tickets = check_other_tickets(input_split[2], ranges)
    # star 1:
    print('Error rate: {}'.format(error_rate))

if __name__ == "__main__":
  main()
