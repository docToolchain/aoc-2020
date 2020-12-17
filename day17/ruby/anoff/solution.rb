#!/usr/bin/ruby
require_relative "./layer.rb"
require_relative "./pocketdimension.rb"

def readInput(path)
  input = File.read(path)
  return input
end

def part1 (map)
  pd = PocketDimension.new
  l = Layer.new(0)
  l.switchTo(map)
  pd.addLayer(l)
  for i in 1..6
    pd.cycle
  end
  return pd.activeCount
end

if __FILE__ == $PROGRAM_NAME
  map = readInput("./input.txt")
  puts "Solution for part1: %d" % part1(map)
end