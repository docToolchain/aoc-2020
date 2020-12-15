#!/usr/bin/ruby

def part1 (input)
  store = Hash.new # create hashmap of number->turn it was spoken
  lastNumber = -1
  for turn in (0..2020-1) # 2020 - 1, because we use 0 indexing
    if turn <= (input.size-1)
      if turn > 0
        store[lastNumber] = turn - 1
      end
      lastNumber = input[turn]
    else
      # p "lastNumber: #{lastNumber}, store:#{store[lastNumber]}, turn:#{turn-1}"
      diff = store[lastNumber].nil? ? 0 : turn-1 - store[lastNumber]
      store[lastNumber] = turn - 1
      lastNumber = diff
    end
  end
  return lastNumber
end

def part2 (input)
  store = Hash.new # create hashmap of number->turn it was spoken
  lastNumber = -1
  for turn in (0..30000000-1) # X - 1, because we use 0 indexing
    if turn <= (input.size-1)
      if turn > 0
        store[lastNumber] = turn - 1
      end
      lastNumber = input[turn]
    else
      # p "lastNumber: #{lastNumber}, store:#{store[lastNumber]}, turn:#{turn-1}"
      diff = store[lastNumber].nil? ? 0 : turn-1 - store[lastNumber]
      store[lastNumber] = turn - 1
      lastNumber = diff
    end
  end
  return lastNumber
end

if caller.length == 0
  puts "Solution for part1: %d" % part1([1,2,16,19,18,0])
  puts "Solution for part2: %d" % part2([1,2,16,19,18,0])
end