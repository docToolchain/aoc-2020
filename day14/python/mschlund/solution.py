import itertools

def get_cmd(line):
  assignment = [x.strip() for x in line.split('=')]
  cmd = assignment[0]

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

def update_mem_andor(mem, loc, val, or_mask, and_mask):
  mem[loc] = (val | or_mask) & and_mask
  return mem

def res_char(x, m):
  if m == '0':
    return x
  else:
    return m

def get_res_with_wildcards(val, mask):
  bin_str = f'{val:036b}'.format(val)
  return ''.join([res_char(x,m) for (x, m) in zip(bin_str, mask)])

# https://www.geeksforgeeks.org/generate-all-binary-strings-from-given-pattern/
def gen_binary(s):
  res = []
  gen_binary_h(s, res)
  return res

def gen_binary_h(s, res):
  if 'X' in s:
    s0 = s.replace('X', '0', 1)
    s1 = s.replace('X', '1', 1)
    gen_binary_h(s0, res)
    gen_binary_h(s1, res)
  else:
    res.append(s)

def update_mem_wildcard(mem, loc, val, mask_with_wildcards):
  loc_with_wildcards = get_res_with_wildcards(loc, mask_with_wildcards)
  all_locations = gen_binary(loc_with_wildcards)
  for l in all_locations:
    mem[int(l, 2)] = val
  return mem

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
      mem = update_mem_andor(mem, parts[0], parts[1], or_mask, and_mask)
  print('Sum of all values in memory (star 1): {}'.format(sum(mem.values())))
  print('-----------------------')

  # star 2:
  mem = {}
  for line in all_lines:
    cmd, parts = get_cmd(line)
    if cmd == 'mask':
      mask_with_wildcards = parts[0]
    else:
      mem = update_mem_wildcard(mem, parts[0], parts[1], mask_with_wildcards)
  print('Sum of all values in memory (star 1): {}'.format(sum(mem.values())))


# end::main[]

if __name__ == "__main__":
  main()
