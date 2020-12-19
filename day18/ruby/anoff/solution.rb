#!/usr/bin/ruby

def readInput(path)
  input = File.read(path)
    .split("\n")

  return input
end

def part1 (input)
  sum = 0
  for line in input
    result = calc(line)
    sum += result
  end
  return sum
end

def calc(input, stopAtParenthesesClose=false)
  eq = input.gsub(/\s/, "") # remove all spaces
  result = 0
  operation = "+"
  i = 0
  while i < eq.size
    char = eq[i]
    if ["+", "*"].include?(char)
      operation = char
    elsif char == "("
      innerResult, offset = calc(eq[(i+1)..-1], stopAtParenthesesClose=true)
      i += offset
      case operation
      when "+"
        result += innerResult
      when "*"
        result *= innerResult
      end
    elsif char == ")" && stopAtParenthesesClose
      return result, i+1
    elsif char.to_i.to_s == char
      case operation
      when "+"
        result += char.to_i
      when "*"
        result *= char.to_i
      end
    else
      throw "Unexpected character: #{char}"
    end
    i += 1
  end
  return result
end
if __FILE__ == $PROGRAM_NAME
  input = readInput("./input.txt")
  puts "Solution for part1: %d" % part1(input)
  #puts "Solution for part2: #{part2(input)}"
end