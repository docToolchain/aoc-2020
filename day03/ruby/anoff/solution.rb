#!/usr/bin/ruby

def readInput(path)
  input = File.read(path)
  input.split("\n")
end

def route (map, startPos, route)
  xMax = map[0].size
  yMax = map.size - 1

  xPos = startPos[0]
  yPos = startPos[1]

  treeCount = 0

  loop do
    xPos += route[0]
    yPos += route[1]
    if xPos >= xMax
      xPos -= xMax
    end
   # puts "encountered #{map[yPos][xPos]} at #{xPos},#{yPos}"
    if map[yPos][xPos] == "#"
      treeCount += 1
    end
    if yPos >= yMax
      break
    end
  end
  treeCount
end

def part1 (input)
  route(input, [0, 0], [3, 1])
end

def part2 (input)
  route(input, [0, 0], [1, 1]) * \
  route(input, [0, 0], [3, 1]) * \
  route(input, [0, 0], [5, 1]) * \
  route(input, [0, 0], [7, 1]) * \
  route(input, [0, 0], [1, 2])
end

if caller.length == 0
  map = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(map)
  puts "Solution for part2: %d" % part2(map)
end