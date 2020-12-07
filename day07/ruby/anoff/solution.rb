#!/usr/bin/ruby
require_relative './ruleset'

def readInput(path)
  input = File.read(path).split("\n")
  return input
end

def part1 (input)
  r = Ruleset.new(input)
  r.expandRules

  return r.bags
    .filter{ |b| b.canContain?("shiny gold") }
    .size
end

def part2 (input)
  r = Ruleset.new(input)
  r.expandRules

  return r.getBag("shiny gold").contentSize
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: %d" % part2(input)
end