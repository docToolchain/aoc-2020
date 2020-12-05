#!/usr/bin/ruby

def readInput(path)
  input = File.read(path)
  input.split("\n")
end

def binSpace2RowCol (input)
  input = input.split("")
  rows = (0..127).to_a
  for char in input[0, 7]
    case char
    when "F"
      rows = rows[0, rows.size/2]
    when "B"
      rows = rows[rows.size/2, rows.size/2]
    else
      puts "Neither F nor B for row assignment: #{char} (#{input.join('')}"
    end
  end
  columns = (0..7).to_a
  for char in input[7, 3]
    case char
    when "R"
      columns = columns[columns.size/2, columns.size/2]
    when "L"
      columns = columns[0, columns.size/2]
    else
      puts "Neither L nor R for column assignment: #{char} (#{input.join('')}"
    end
  end
  return rows.append(columns[0])
    map(&:to_i)
end

def binSpace2seatId (binSpace)
  row, col = binSpace2RowCol(binSpace)
  return row * 8 + col
end

def part1 (input)
  input
    .map{|binSpace| binSpace2seatId(binSpace)}
    .max
end

def part2 (input)
  route(input, [0, 0], [1, 1]) * \
  route(input, [0, 0], [3, 1]) * \
  route(input, [0, 0], [5, 1]) * \
  route(input, [0, 0], [7, 1]) * \
  route(input, [0, 0], [1, 2])
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  #puts "Solution for part2: %d" % part2(input)
end