#!/usr/bin/ruby
require_relative "./rule.rb"

def readInput(path)
  rules, ticketMine, ticketsNearby = File.read(path).split("\n\n")
  return rules.split("\n"), ticketMine.split("\n")[1], ticketsNearby.split("\n")[1..-1]
end

def part1 (rules, ticketMine, ticketsNearby)
  rs = RuleSet.new
  for rule in rules
    name, ranges = rule.split(": ")
    range1, range2 = ranges.split(" or ")
    r = Rule.new(name, range1, range2)
    rs.add(r)
  end
  
  errorRate = 0
  for ticket in ticketsNearby
    for value in ticket.split(",")
      if not rs.valid?(value.to_i)
        errorRate += value.to_i
      end
    end
  end
  return errorRate
end

def part2 (input)

end

if caller.length == 0
  rules, ticketMine, ticketsNearby = readInput("./input.txt")
  puts "Solution for part1: %d" % part1(rules, ticketMine, ticketsNearby)
  #puts "Solution for part2: %d" % part2([1,2,16,19,18,0])
end