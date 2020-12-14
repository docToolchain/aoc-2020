#!/usr/bin/ruby

def readInput(path)
  input = File.read(path)
    .split("\n")
  return input
end

def maskedValue(mask, value)
  andMask = mask.gsub(/X/, "1").to_i(base=2)
  orMask = mask.gsub(/X/, "0").to_i(base=2)

  return (value & andMask) | orMask
end

def part1(input)
  mask = 0
  data = {}
  for line in input
    if !(line =~ /^mask/).nil?
      mask = line.split(" = ")[1]
    else
      id, val = line.match(/mem\[([0-9]+)\]\s=\s([0-9]+)/).captures
      data[id] = maskedValue(mask, val.to_i)
    end
  end
  data.values
    .reduce(&:+)
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  # puts "Solution for part2: %d" % part2(input)
end