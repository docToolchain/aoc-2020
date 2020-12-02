import java.io.File

// tag::passwd_list[]
fun passwd_list(): Int {
	var passwd: String
	var letter: String
	var start: Int
	var end: Int
	var result: Int = 0

	File("day2002_puzzle_input.txt").forEachLine {
		var instruction = it.split(" ")
		passwd = instruction[2]
		letter = instruction[1].dropLast(1)
		var range = instruction[0].split("-")
		start = range[0].toInt()
		end = range[1].toInt()

		if (passwd.length - passwd.replace(letter, "").length >= start && passwd.length - passwd.replace(
				letter,
				""
			).length <= end
		) {
			result++
		}

	}
	return result
}
// end::passwd_list[]

// tag::passwd_list_2[]
fun passwd_list_2(): Int {
	var passwd: String
	var letter: String
	var start: Int
	var end: Int
	var result: Int = 0

	File("day2002_puzzle_input.txt").forEachLine {
		var instruction = it.split(" ")
		passwd = instruction[2]
		letter = instruction[1].dropLast(1)
		var range = instruction[0].split("-")
		start = range[0].toInt() - 1
		end = range[1].toInt() - 1

		if (passwd[start].toString().equals(letter) && !passwd[end].toString().equals(letter) || !passwd[start].toString().equals(
				letter
			) && passwd[end].toString().equals(letter)
		) {
			result++
		}
	}
	return result
}
// end::passwd_list_2[]


//fun main(args: Array<String>) {
	var solution1: Int
	var solution2: Int


// tag::part_1[]
	solution1 = passwd_list()
// end::part_1[]

// tag::part_2[]
	solution2 = passwd_list_2()
// end::part_2[]


// tag::output[]
// print solution for part 1
	println("****************************")
	println("--- Day 2: Password Philosophy ---")
	println("****************************")
	println("Solution for part1")
	println("   $solution1 passwords are valid according to their policies")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 passwords are valid according to the new interpretation of the policies")
	println()
// end::output[]
//}