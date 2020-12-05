#!/usr/bin/ruby
def validate_passport_fields_exist(passport)
  mandatoryFields = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"
    #"cid"
  ]

  for field in mandatoryFields
    if not passport.include? (field + ":")
      # puts "did not find #{field} in passport '#{passport}'"
      return false
    end
  end
  return true
end

def validate_passport_field_values(passport)
  passport.split(" ").each { |field|
    key, value = field.split(":")
    case key
    when "byr"
      v = value.to_i
      if value.size != 4 || v < 1920 || v > 2002
        #puts "!Inorrect passport field: #{field}"
        return false
      end
    when "iyr"
      v = value.to_i
      if value.size != 4 || v < 2010 || v > 2020
        #puts "!Inorrect passport field: #{field}"
        return false
      end
    when "eyr"
      v = value.to_i
      if value.size != 4 || v < 2020 || v > 2030
        #puts "!Inorrect passport field: #{field}"
        return false
      end
    when "hgt"
      v = value.to_i
      if !(v >= 150 && v <= 193 && value.split("").last(2).join("") == "cm") && !(v >= 59 && v <= 76 && value.split("").last(2).join("") == "in")
        #puts "!Inorrect passport field: #{field}"
        return false
      end
    when "hcl"
      if not value =~ /#[a-f0-9]{6}/
        #puts "!Inorrect passport field: #{field}"
        return false
      end
    when "ecl"
      if not ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"].include? value
        #puts "!Inorrect passport field: #{field}"
        return false
      end
    when "pid"
      if not value =~ /^[0-9]{9}$/
        #puts "!Inorrect passport field: #{field}"
        return false
      end
    end
    # puts "Correct passport field: #{field}"
  }
  return true
end
# turn text into an array of passports
#   each passport is a string with the elements separated by " "
def parse_text(text)
  passports = text
    .split("\n\n")
    .map { |entry|
      entry.gsub("\n", " ")
    }
  
end

def part1(input)
  passports = parse_text(input)
  passports
    .filter { |passport| validate_passport_fields_exist(passport)}
    .size
end

def part2(input)
  passports = parse_text(input)
  passports
    .filter { |passport| validate_passport_fields_exist(passport)}
    .filter { |passport| validate_passport_field_values(passport)}
    .size
end

if caller.length == 0
  input = File.read("./input.txt")

  puts "Solution for part1: %d" % part1(input)
  puts "Solution for part2: %d" % part2(input) # 130, 88, 138
end