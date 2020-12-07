#!/usr/bin/ruby

def readInput(path)
  input = File.read(path)
  return input
end

def parseGroups(input)
  input
    .split("\n\n")
    .map{ |group|
      group.split("\n").join("")
    }
end

def mergeGroupAnswers(groups)
  groups
    .map{ |group| group.split("").sort.join("") }
    .map{ |group| group.gsub(/(\w)\1+/, '\1') }
end

def part1 (input)
  mergeGroupAnswers(parseGroups(input))
    .map{ |g| g.size }
    .reduce(0, &:+)
end

def part2 (input)
  groups = input.split("\n\n")
  groups.map{ |g|
    groupSize = g.split("\n").size
    answersSorted = g.split("").sort.join("").gsub("\n", "")
    answerCount = 0
    for char in answersSorted.gsub(/(\w)\1+/, '\1').split("")
      if answersSorted.include?(char * groupSize)
        answerCount += 1
      end
    end
    # puts "sum:#{answerCount} for size:#{groupSize} (#{answersSorted})"
    answerCount
  }
  .reduce(&:+)
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: %d" % part2(input)
end