#!/usr/bin/ruby

def readInput(path)
  input = File.read(path).split("\n").map(&:to_i)
  return input
end

# check if `number` is the sum of any two values provided in `range`
def validNumber?(range, number)
  range = range.sort
  ix2 = range.size - 1
  for ix1 in (0..(range.size-1)).to_a
    for ix2 in (0..(range.size-1)).to_a.reverse
      if ix1 == ix2
        next
      end
      n = range[ix1] + range[ix2]
      if n == number
        return true
      end
      if n < number # speed improvement, if upper pointer + lower pointer return a too low number move the upper pointer forward
        break
      end
    end
  end
  return false
end

def part1 (input, windowSize)
  for i in (windowSize..(input.size - 1)).to_a
    #windowIx = (0..(windowSize-1))#.to_a.map{ |n| n + (i - windowSize) }
    windowIx = ((i-windowSize)..(i-1))
    window = input[windowIx]
    number = input[i]
    if not validNumber?(window, number)
      return input[i]
    end
  end
end

# find a contiguous range of numbers in `input` that sums up to `sum`
def findRangeForSum(input, sum)
  for windowSize in 2..(input.size - 1)
    for ix in 0..(input.size - 1 - windowSize)
      window = (ix..(ix+windowSize))
      n = input[window].reduce(&:+)
      if n == sum
        return input[window]
      end
    end
  end
end

def part2 (input, targetNumber)
  window = findRangeForSum(input, targetNumber).sort
  return window[0] + window[-1]
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input, 25)
  puts "Solution for part2: %d" % part2(input, 14360655)# 1631469 too low
end