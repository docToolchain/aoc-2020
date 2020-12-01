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
    return nil
end

def part2(input)
  sorted = input
    .filter { |val| val < 2020 }
    .sort

  sorted
    .reverse
    .each { |bigVal|
      puts "new val: %d" % bigVal
      ix1 = 0
      ix2 = 1
      sum = bigVal + sorted[ix1] + sorted[ix2]
      while ix1 < sorted.size do
        ix2 = 0
        ix1 += 1
        while sum < 2020 do
          ix2 += 1
          if ix2 == ix1
            ix2 += 1
          end
          puts "ix1: %d, ix2: %d" % [ix1, ix2]
          sum = bigVal + sorted[ix1] + sorted[ix2]
          if ix2 == sorted.size-1
            puts "breaking inner loop"
            break
          end
        end
        #puts "ix1: %d, ix2: %d" % [ix1, ix2]
        
        puts "%d for %d + %d+%d (%d|%d)" % [sum, bigVal, sorted[ix1], sorted[ix2], ix1, ix2]
        # if ix2 == 0
        #   puts "breaking outer loop at sum:%d w/ ix2:%d" % [sum, ix2]
        #   break
        # end
        if sum == 2020
          return bigVal * sorted[ix1] * sorted[ix2]
        end
      end
    }
    return -1
end

if caller.length == 0
  input = File.read("./input.txt")

  expenses = input.split("\n").map(&:to_i)

  #puts "Solution for part1: %d" % part1(expenses)
  puts "Solution for part2: %d" % part2(expenses)
end