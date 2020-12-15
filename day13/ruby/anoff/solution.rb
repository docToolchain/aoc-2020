#!/usr/bin/ruby

def readInput(path)
  input = File.read(path)
    .split("\n")
  return input
end

def timeUntilDeparture(busID, t)
  t%busID != 0 ? busID - t%busID : 0
end
def part1 (input)
  t, busIDs = input
  t = t.to_i
  minTime, busIx = busIDs
    .split(",")
    .map{ |id|
      if id == "x"
        1e4 # some arbitrary "large" number
      else
        timeUntilDeparture(id.to_i, t)
      end
    }
    .each_with_index
    .min
  busID = busIDs.split(",")[busIx].to_i
  minTime * busID
end

def part2 (input)
  ids = input
    .split(",")
    .map.with_index{ |id, ix|
      { id: id.to_i, offset: ix }
    }
    .filter{ |b|
      b[:id] > 0
    }
  t = 0
  dt = 1
  for b in ids
    while (t + b[:offset]) % b[:id] != 0
      t += dt
    end
    dt *= b[:id] # increase increment for each step by busid to make sure all future timesteps are multiples of the previous schedule
    puts "Included bus #{b}"
  end
  return t
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: %d" % part2(input[1])
end