#!/usr/bin/ruby
require_relative "./allergenmap.rb"

def readInput(path)
  input = File.read(path).split("\n")
  return input
end

def part1 (input)
  am = AllergenMap.new(input)
  allergens = am.allergens.values
  nonAllergenicCount = 0
  for line in input
    ingredients = line.split(" (contains")[0].split(" ")
    nonAllergenicCount += ingredients
      .filter{|i| not allergens.include?(i)}
      .size
  end
  return nonAllergenicCount
end


def part2 (input)
  am = AllergenMap.new(input)
  am.allergens
    .keys.sort
    .map{|k| am.allergens[k]}
    .join(",")
end

if __FILE__ == $PROGRAM_NAME
  input = readInput("./input.txt")
  puts "Solution for part1: #{part1(input)}"
  puts "Solution for part2: #{part2(input)}"
end
