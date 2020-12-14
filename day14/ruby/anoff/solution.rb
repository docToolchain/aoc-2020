#!/usr/bin/ruby

def readInput(path)
  input = File.read(path)
    .split("\n")
  return input
end

def maskedValue(mask, value)
  andMask = mask.gsub(/X/, "1").to_i(base=2)
  orMask = mask.gsub(/X/, "0").to_i(base=2)

  return (value & andMask) | orMask
end

def part1(input)
  mask = 0
  data = {}
  for line in input
    if !(line =~ /^mask/).nil?
      mask = line.split(" = ")[1]
    else
      id, val = line.match(/mem\[([0-9]+)\]\s=\s([0-9]+)/).captures
      data[id] = maskedValue(mask, val.to_i)
    end
  end
  data.values
    .reduce(&:+)
end

def addressModifier(mask, address)
  def toggleX(mask)
    xIx = mask.split("").find_index{ |v| v == "X" }
    if xIx.nil?
      return [mask.to_i(base=2)]
    end
    mask1 = mask.dup
    mask1[xIx] = "0"
    mask2 = mask.dup
    mask2[xIx] = "1"
    return toggleX(mask1) + toggleX(mask2)
  end
  mask = mask.dup
  aString = "%036d" % address.to_s(base=2)
  for ix in 0..35
    if mask[ix] == "0" && aString[ix] == "1"
      mask[ix] = "1"
    end
  end
  maskVariations = toggleX(mask)
  return maskVariations
end

def part2(input)
  mask = 0
  data = {}
  for line in input
    if !(line =~ /^mask/).nil?
      mask = line.split(" = ")[1]
    else
      address, val = line.match(/mem\[([0-9]+)\]\s=\s([0-9]+)/).captures
      val = val.to_i
      address = address.to_i
      addresses = addressModifier(mask, address)
      for id in addresses
        data[id] = val
      end
    end
  end
  data.values
    .reduce(&:+)
end

if caller.length == 0
  input = readInput("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: %d" % part2(input) # 2662888623651 too low
end