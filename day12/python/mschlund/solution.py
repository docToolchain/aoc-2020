DIRS = ['E', 'S', 'W', 'N']

def init():
  ship_pos = (0,0) # x-dir: +-1 for E/W, y-dir +-1 for N/S
  direction = 0 # 0=E, 1=S, 2=W, 3=N
  return ship_pos, direction

def pos_shift(pos, direction, steps):
  if DIRS[direction] == 'E':
    return (pos[0] + steps, pos[1])
  elif DIRS[direction] == 'S':
    return (pos[0], pos[1] - steps)
  elif DIRS[direction] == 'W':
    return (pos[0] - steps, pos[1])
  elif DIRS[direction] == 'N':
    return (pos[0], pos[1] + steps)

def execute_movement_1(ship_pos, direction, line):
  cmd = line[0]
  num = int(line[1:])
  if cmd == 'F':
    new_pos = pos_shift(ship_pos, direction, num)
    new_dir = direction
  elif cmd in ['N', 'S', 'E', 'W']:
    new_pos = pos_shift(ship_pos, DIRS.index(cmd), num)
    new_dir = direction
  elif cmd == 'L':
    new_pos = ship_pos
    new_dir = int((direction - num/90)) % 4
  elif cmd == 'R':
    new_pos = ship_pos
    new_dir = int((direction + num/90)) % 4
  return new_pos, new_dir

  def execute_movement_2(pos, stride, direction, line):
    cmd = line[0]
    num = int(line[1:])
    

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    movements = [l for l in input]
    ship_pos, direction = init()
    # star 1:
    for m in movements:
      ship_pos, direction = execute_movement_1(ship_pos, direction, m)
      print('Pos: {}, Dir: {}'.format(ship_pos, DIRS[direction]))
      dist_to_origin = abs(ship_pos[0]) + abs(ship_pos[1])
      print('Distance to origin = {}'.format(dist_to_origin))
    # star 2:
    stride = (10, 1)
    for m in movements:
      pos, stride, direction = execute_movement_2(pos, stride, direction, m)


if __name__ == "__main__":
  main()
