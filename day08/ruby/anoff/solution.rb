#!/usr/bin/ruby
require_relative './computer'

def readInput(path)
  input = File.read(path).split("\n")
  return input
end

def part1 (input)
  c = Computer.new(input)
  while c.step == 0
    c.step
  end
  return c.acc
end

def part2 (input)
  c = Computer.new(input)
  while c.step == 0
    c.step
  end

  # change each executed command (from the back) to either nop/jmp and try rerunning the operations
  for ptr in c.ptrHistory.reverse
    modified_input = input
    code, value = modified_input[ptr].split(" ")
    # switch jmp <-> nop
    case code
    when "nop"
      modified_input[ptr] = "jmp #{value}"
    when "jmp"
      modified_input[ptr] = "nop #{value}"
    else
      # for other operations, skip this loop
      next
    end
    c2 = Computer.new(modified_input)
    returnCode = c2.run
    # return 1 means end of program is reached
    if returnCode == 1
      puts "Successfully terminated"
      return c2.acc
    end
  end
end

if caller.length == 0
  input = readInput("./input.txt")

  #puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: %d" % part2(input)
end