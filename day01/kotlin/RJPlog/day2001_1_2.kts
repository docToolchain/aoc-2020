import java.io.File

// tag::add_two_coins[]
fun add_two_coins(): Int {
	var result: Int = 0
	File("day2001_puzzle_input.txt").forEachLine {
		var mul_1 = it.toInt()
		File("day2001_puzzle_input.txt").forEachLine {
			var mul_2 = it.toInt()
			if (mul_1 != mul_2) {
				if ((mul_1 + mul_2) == 2020) {
					result = mul_1 * mul_2
				}
			}
		}
	}
	return result
}
// end::add_two_coins[]

// tag::add_three_coins[]
fun add_three_coins(): Int {
	var result: Int = 0
	File("day2001_puzzle_input.txt").forEachLine {
		var mul_1 = it.toInt()
		File("day2001_puzzle_input.txt").forEachLine {
			var mul_2 = it.toInt()
			File("day2001_puzzle_input.txt").forEachLine {
				var mul_3 = it.toInt()
				if (mul_1 != mul_2 && mul_1 != mul_3) {
					if ((mul_1 + mul_2 + mul_3) == 2020) {
						result = mul_1 * mul_2 * mul_3
					}
				}
			}
		}
	}
	return result
}
// end::add_three_coins[]


//fun main(args: Array<String>) {
	var solution1: Int
	var solution2: Int

// tag::part_1[]
	solution1 = add_two_coins()
// end::part_1[]

// tag::part_2[]
	solution2 = add_three_coins()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("****************************")
	println("--- Day 1: Report Repair ---")
	println("****************************")
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