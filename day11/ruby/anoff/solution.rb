#!/usr/bin/ruby
require_relative './seats'

def readInput(path)
  input = File.read(path)
    .split("\n")
    .map{ |line| line.split("") } # make sure we get an array of arrays not a string
  return input
end

def part1 (input)
  s = Seatmap.new(input)
  count = -1
  while count != s.totalOccupiedSeatCount
    count = s.totalOccupiedSeatCount
    s.step
  end
  count
end

def part2 (input)
  s = Seatmap2.new(input)
  count = -1
  while count != s.totalOccupiedSeatCount
    count = s.totalOccupiedSeatCount
    s.step
  end
  count
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: %d" % part2(input)
end