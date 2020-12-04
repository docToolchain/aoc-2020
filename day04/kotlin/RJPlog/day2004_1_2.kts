import java.io.File

// tag::count_valid[]
fun count_valid(): Int {
	var count: Int = 0
	var fields = mutableListOf<String>()

	File("day2004_puzzle_input.txt").forEachLine {
		var instruction = it.split(" ")
		for (i in 0..instruction.size - 1) {
			var data = instruction[i].split(":")
			fields.add(data[0])
		}
		if (it == "") {
			if (fields.contains("byr") && fields.contains("iyr") && fields.contains("eyr") && fields.contains("hgt") && fields.contains(
					"hcl"
				) && fields.contains("ecl") && fields.contains("pid")
			) {
				count++
			}
			fields.clear()
		}
	}
	return count
}
// end::count_valid[]

// tag::count_valid_2[]
fun count_valid_2(): Int {
	var count: Int = 0
	var fields = mutableListOf<String>()

	File("day2004_puzzle_input.txt").forEachLine {
		var instruction = it.split(" ")
		for (i in 0..instruction.size - 1) {
			var data = instruction[i].split(":")
			if (data[0].equals("byr") && (data[1].toInt() >= 1920 && data[1].toInt() <= 2002)) {
				fields.add(data[0])
			} else if (data[0].equals("iyr") && (data[1].toInt() >= 2010 && data[1].toInt() <= 2020)) {
				fields.add(data[0])
			} else if (data[0].equals("eyr") && (data[1].toInt() >= 2020 && data[1].toInt() <= 2030)) {
				fields.add(data[0])
			} else if (data[0].equals("hgt")) {
				if (data[1].takeLast(2).equals("cm") && (data[1].dropLast(2).toInt() >= 150 && data[1].dropLast(2).toInt() <= 193)) {
					fields.add(data[0])
				} else 	if (data[1].takeLast(2).equals("in") && (data[1].dropLast(2).toInt() >= 59 && data[1].dropLast(2).toInt() <= 76)) {
					fields.add(data[0])
				}
			} else if (data[0].equals("hcl") && data[1].length == 7 ) {
				fields.add(data[0])
			} else if (data[0].equals("ecl") && (data[1].contains("amb") || data[1].contains("blu") || data[1].contains("brn")|| data[1].contains("gry")|| data[1].contains("grn")|| data[1].contains("hzl")|| data[1].contains("oth"))) {
				fields.add(data[0])
			} else if (data[0].equals("pid") && (data[1].length == 9)) {
				var pid_ok = true
				data[1].forEach{
					if (!it.isDigit()) {
					pid_ok = false	
					}
				}
				if (pid_ok) {
				fields.add(data[0])  }
				pid_ok = true
			}

		}
		if (it == "") {
			if (fields.contains("byr") && fields.contains("iyr") && fields.contains("eyr") && fields.contains("hgt") && fields.contains(
					"hcl"
				) && fields.contains("ecl") && fields.contains("pid")
			) {
				count++
			}
			fields.clear()
		}
	}
	return count
}
// end::count_valid_2[]


//fun main(args: Array<String>) {
	var solution1: Int 
	var solution2: Int 

// tag::part_1[]
	solution1 = count_valid()
// end::part_1[]

// tag::part_2[]
	solution2 = count_valid_2()
// end::part_2[]

// tag::output[]
	println("**********************************")
	println("--- Day 4: Passport Processing ---")
	println("**********************************")
	println("Solution for part1")
	println("   $solution1 ")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2")
	println()
// end::output[]
//}		