#!/usr/bin/ruby
require_relative './ship'

def readInput(path)
  input = File.read(path)
    .split("\n")
  return input
end

def part1 (input)
  s = Ship.new
  for instruction in input
    s.move(instruction)
  end
  s.pos.x.abs + s.pos.y.abs
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
  #puts "Solution for part2: %d" % part2(input)
end