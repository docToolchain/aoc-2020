
def decode_seat(line):
  row_binary = line[:7].replace('F', '0').replace('B', '1')
  col_binary = line[7:].replace('L', '0').replace('R', '1')
  row = int(row_binary, 2)
  col = int(col_binary, 2)
  return row, col

def get_ids_dist_2(id_list):
  sorted_ids = sorted(id_list)
  pos_to_id = dict(enumerate(sorted_ids))
  successive_ids = [(pos_to_id[i], pos_to_id[i+1])  for i in range(len(id_list)-1 ) ]
  ids_2_apart = [x for x in successive_ids if abs(x[0]-x[1]) == 2]
  return ids_2_apart

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    ids = []
    for line in input:
      row, col = decode_seat(line)
      seat_id = row*8 + col
      ids.append(seat_id)
    neighboring_ids = get_ids_dist_2(ids)
    assert(len(neighboring_ids) == 1)
    my_id = int((neighboring_ids[0][1] + neighboring_ids[0][0])/2)
    max_id = max(ids)
    print('Max id: {}'.format(max_id))
    print('My seat: {}'.format(my_id))

if __name__ == "__main__":
  main()