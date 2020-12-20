import numpy as np
import scipy.ndimage
from functools import partial


def count_occupied(values):
  return sum([x == 1 for x in values])

def result_state_regular(values, threshold = 4):
  arr = np.reshape(values, (3,3))
  if arr[1,1] == 0:
    return all([x in [0, 2] for x in values])*1
  elif arr[1,1] == 1:
    arr_real = arr[arr != 2]
    return ((arr_real.sum() - 1) < threshold)*1
  else:
    return 2

def update_board_1(board):
  return scipy.ndimage.generic_filter(board, result_state_regular, size=3, cval=2, mode='constant')

def iterate_until_stable(board, step_function):
  new_board = step_function(board)
  stable = (board == new_board).sum() == board.shape[0]*board.shape[1]
  board = new_board
  while not stable:
    new_board = step_function(board)
    stable = (board == new_board).sum() == board.shape[0]*board.shape[1]
    board = new_board
  return new_board

def get_seat_in_line(starting_point, dx, dy, board):
  current_pos = starting_point
  while True:
    new_pos = current_pos + np.array((dx,dy))
    if (new_pos[0] < board.shape[0] and 
        new_pos[1] < board.shape[1] and 
        new_pos[0] >= 0 and 
        new_pos[1] >= 0):
      idx = (new_pos[0], new_pos[1])
      if board[idx] == 0:
        return idx
      else:
        current_pos = new_pos
    else:
      return (-1,-1)

def compute_neighborhoods(board):
  strides = [(-1,-1), (0,-1), (+1,-1),
             (-1,0),          (+1,0),
             (-1,+1), (0,+1), (+1,+1)]
  rows, cols = np.where(board == 0) # get indices of seats
  neighborhoods = {}
  for x,y in zip(rows, cols):
    neighbors = []
    for (dx,dy) in strides:
      starting_point = np.array((x,y))
      sx, sy = get_seat_in_line(starting_point, dx, dy, board)
      if sx != -1 and sy != -1:
        neighbors.append((sx, sy))
    neighborhoods[(x,y)] = neighbors
  return neighborhoods

def result_state(current_state, neighborhood, board, threshold = 5):
  real_neighbors = [board[x] for x in neighborhood]
  if current_state == 0:
    return (sum(real_neighbors) == 0)*1
  elif current_state == 1:
    return (sum(real_neighbors) < threshold)*1
  else:
    return 2

def update_board_2(neighborhoods, seats, board):
  new_board = board.copy()
  for x,y in seats:
    new_board[x,y] = result_state(board[x,y], neighborhoods[(x,y)], board)
  return new_board

def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    string_board = np.genfromtxt(input, delimiter=1, dtype=str)
    string_board_1 = np.char.replace(string_board, 'L', '0')
    string_board_2 = np.char.replace(string_board_1, '.', '2')
    board = string_board_2.astype(int)

    # star 1:
    result_stable = iterate_until_stable(board, update_board_1)
    num_occupied = result_stable[result_stable == 1].sum()
    print('{} seats occupied (star 1).'.format(num_occupied))

    # star 2:
    neighborhoods = compute_neighborhoods(board)
    rows, cols = np.where(board == 0) # get indices of seats
    seats = [(x,y) for x,y in zip(rows, cols)]
    update_fcn = partial(update_board_2, neighborhoods, seats)
    result_stable = iterate_until_stable(board, update_fcn)
    num_occupied = result_stable[result_stable == 1].sum()
    print('{} seats occupied (star 2).'.format(num_occupied))    


if __name__ == "__main__":
  main()
