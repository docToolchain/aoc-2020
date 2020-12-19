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

def calc2(input)
  eq = input.gsub(/\s/, "") # remove all spaces
  while eq.to_i.to_s != eq
    p eq
    # first solve all additions that do not involve parenthesis
    eq = eq.gsub(/(\d+)\+(\d+)/) { |match|
      a, b = match.split("+")
      a.to_i + b.to_i
    }
    # remove useless parentheses
    eq = eq.gsub(/\((\d+)\)/, '\1')
    # multiply only within parentheses
    eq = eq.gsub(/\((\d+)\*(\d+)\)/) { |match|
      a, b = match.split("*")
      a[1..-1].to_i * b[0..-2].to_i
    }
    # remove useless parentheses
    eq = eq.gsub(/\((\d+)\)/, '\1')
    # handle parenthesis recursively
    eq = eq.gsub(/\([\d\+\*]+\)/) { |match|
      subeq = match[1..-2] # remove parentheses
      calc2(subeq)
    }
    # remove useless parentheses
    eq = eq.gsub(/\((\d+)\)/, '\1')
    # only after all + and () have been solved start multiplying stuff
    if not (eq.include?("+") || eq.include?("("))
      eq = eq.gsub(/(\d+)\*(\d+)/) { |match|
        a, b = match.split("*")
        a.to_i * b.to_i
      }
    end

    # remove useless parentheses
    eq = eq.gsub(/\((\d+)\)/, '\1')
  end
  return eq.to_i
end

def part2 (input)
  sum = 0
  for line in input
    result = calc2(line)
    sum += result
  end
  return sum
end

if __FILE__ == $PROGRAM_NAME
  input = readInput("./input.txt")
  puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: #{part2(input)}"
end