#!/usr/bin/ruby
def validate_password(password, policy)
  parts = policy.split(" ")
  policyChar = parts[1]
  min, max = parts[0].split("-").map(&:to_i)

  isCount = password.count(policyChar)
  return isCount >= min && isCount <= max
end

def part1(input)
  input
    .map { |e|
      validate_password(e[:password], e[:policy])
    }
    .count(true)
end

def part2(input)

end

if caller.length == 0
  input = File.read("./input.txt")

  entries = input
    .split("\n")
    .map { |line|
      parts = line.split(": ")
      { policy: parts[0], password: parts[1] }
    }
  puts "Solution for part1: %d" % part1(entries)
  #puts "Solution for part2: %d" % part2(entries)
end