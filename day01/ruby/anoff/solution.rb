#!/usr/bin/ruby
def required_fuel(mass)
  (mass / 3) - 2
end

def part1(input)
  sorted = input
    .filter { |val| val < 2020 }
    .sort

  sorted
    .reverse
    .each { |bigVal|
      ix = 0
      sum = bigVal + sorted[ix]
      while sum < 2020 do
        ix += 1
        sum = bigVal + sorted[ix]
        if ix == sorted.size-1
          break
        end
      end
      if sum == 2020
        return bigVal * sorted[ix]
      end
    }
end

def part2(massInventory)
  fuelSum = 0
  massInventory.each{ |mass|
    fuel = required_fuel(mass)
    while fuel > 0 do
      fuelSum += fuel
      fuel = required_fuel(fuel)
    end
  }
  fuelSum
end

if caller.length == 0
  input = File.read("./input.txt")

  expenses = input.split("\n").map(&:to_i)

  puts "Solution for part1: %d" % part1(expenses)
  #puts "Solution for part2: %d" % part2(massInventory)
end