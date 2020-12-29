import sympy
import sympy.ntheory.modular as mod

# tag::starOne[]
def get_next_bus(t, busses):
  times_to_wait = [(-t % x, x) for x in busses]
  return min(times_to_wait)
# end::star_1[]

# tag::main[]
def main():
  input_filename = 'input.txt'
  with open(input_filename, 'r') as input:
    whole_input = input.read().split('\n')
    time = int(whole_input[0])
    bus_ids = [int(x) for x in whole_input[1].split(',') if x != 'x']
    t, bus_id = get_next_bus(time, bus_ids)
    print((t,bus_id))
    print('Star1: {}'.format(t*bus_id))
    print('-------------------')
    zipped_ids = [(int(x),-i) for i,x in enumerate(whole_input[1].split(',')) if x != 'x']
    m,v = zip(*zipped_ids)
    res = mod.crt(m, v)
    print("Star 2: {}".format(res))
# end::main[]



if __name__ == "__main__":
  main()
