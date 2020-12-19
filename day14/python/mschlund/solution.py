
def get_cmd(line):
  assignment = [x.strip() for x in line.split('=')]
  cmd = assignment[0]
  print(cmd)
  print(assignment)

  if(cmd == 'mask'):
    return cmd, [assignment[1]]
  else:
    loc = int(assignment[0].split('[')[1].rstrip(']'))
    val = int(assignment[1])
    return cmd, [loc, val]

def update_bitmask_1(new_mask):
  and_mask = int(new_mask.replace('X', '1'), 2)
  or_mask = int(new_mask.replace('X', '0'), 2)
  return or_mask, and_mask

def get_transformed_val(val, or_mask, and_mask):
  return (val | or_mask) & and_mask

def update_mem(mem, loc, val, or_mask, and_mask):
  mem[loc] = (val | or_mask) & and_mask
  return mem

def 

# tag::main[]
def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    mem = {}
    all_lines = [line for line in input]

  # star 1:
  for line in all_lines:
    cmd, parts = get_cmd(line)
    if cmd == 'mask':
      or_mask, and_mask = update_bitmask_1(parts[0])
    else:
      print(and_mask, or_mask)
      mem = update_mem(mem, parts[0], parts[1], or_mask, and_mask)
  print('Sum of all values in memory (star 1): {}'.format(sum(mem.values())))
  print('-----------------------')

  # star 2:
  mem = {}
  for line in all_lines:
    cmd, parts = get_cmd(line)
    if cmd == 'mask':
      or_mask, and_mask = update_bitmask_2(parts[0])
    else:
      print(and_mask, or_mask)
      mem = update_mem(mem, parts[0], parts[1], or_mask, and_mask)
  print('Sum of all values in memory (star 1): {}'.format(sum(mem.values())))


# end::main[]

if __name__ == "__main__":
  main()
