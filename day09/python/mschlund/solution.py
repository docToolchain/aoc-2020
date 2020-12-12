class XMASCode:
  def __init__(self, size):
    self._num_elems = 0
    self._buffer = []
    self._sum_pairs = set([])
    self._size = size

  def __str__(self):
    return 'Buf: {}\nSums: {}'.format(str(self._buffer), str(self._sum_pairs))

  def push(self, number):
    if self._num_elems == self._size:
      self._buffer.pop(0) # throw out the first element, if buffer is full
    else:
      self._num_elems += 1
    self._buffer.append(number)

  def is_valid(self, number):
    self._sum_pairs = {x+y for x in self._buffer for y in self._buffer}
    return number in self._sum_pairs

def find_contiguous_seq(all_numbers, target):
  seq = []
  i = 0
  while i < len(all_numbers):
    if sum(seq) == target:
      return seq
    elif sum(seq) < target:
      seq.append(all_numbers[i])
      i += 1
    elif sum(seq) > target:
      seq.pop(0)
  return []

def main():
  input_filename = 'input.txt'
  preamble_length = 25
  with open(input_filename, 'r') as input:
    cnt = 0
    C = XMASCode(preamble_length)
    foundit = False
    all_numbers = []
    for i, line in enumerate(input):
      num = int(line)
      all_numbers.append(num)
      if cnt < preamble_length:
        cnt += 1
      else:
        if not foundit and not C.is_valid(num):
          invalid_num = num
          foundit = True
      C.push(num)

    # star 1:
    print('Invalid-number: {}'.format(invalid_num))

    #star 2:
    seq = find_contiguous_seq(all_numbers, target = invalid_num)

    print('seq found: {}'.format(str(seq)))
    if seq != []:
      print('Result: {}'.format(min(seq) + max(seq)))



if __name__ == "__main__":
  main()
