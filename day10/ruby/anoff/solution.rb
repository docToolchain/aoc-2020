#!/usr/bin/ruby

def readInput(path)
  input = File.read(path).split("\n").map(&:to_i)
  return input
end

# returns an array of how often each difference occurs [1jolt diff, 2joltdiff, 3joltdiff]
#   also checks that no diff is > 3
def joltageDiff(input)
  # add my input device with rating +3
  input.append(input.max + 3)
  arr = input
    .sort
    .reverse
  
  diffs = arr
    .map.with_index{ |n, i|
      if i < arr.size - 1
        n - arr[i+1]
      end
    }
  diffs.pop # remove last element
  # puts diffs.sort
  counts = [0, 0, 0]
  counts[0] = diffs.select{ |n| n == 1 }.size + 1 # fuck knows why this is here.. #dirtyhack
  counts[1] = diffs.select{ |n| n == 2 }.size
  counts[2] = diffs.select{ |n| n == 3 }.size
  #puts counts
  return counts
end

def part1 (input)
  diffs = joltageDiff(input)
  return diffs[0] * diffs[2]
end

def part2 (input, targetNumber)
  window = findRangeForSum(input, targetNumber).sort
  return window[0] + window[-1]
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  #puts "Solution for part2: %d" % part2(input, 14360655)# 1631469 too low
end