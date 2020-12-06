import java.io.File

// tag::group_answers[]
fun group_answers(): Int {
	var count: Int = 0
	var answer = mutableListOf<Char>()

	File("day2006_puzzle_input.txt").forEachLine {
		if (it != "") {
			it.forEach {
				answer.add(it)
			}
		} else if (it == "") {
			count = count + answer.distinct().size
			answer.clear()
		}
	}
	return count
}
// end::group_answers[]

// tag::group_answers_2[]
fun group_answers_2(): Int {
	var count: Int = 0
	var answer = mutableListOf<Char>()
	var answer_new = mutableListOf<Char>()
	var entry: Int = 1

	File("day2006_puzzle_input.txt").forEachLine {
		if (it != "" && entry == 1) {
			it.forEach {
				answer.add(it)
			}
			entry = 0
		} else if (it != "" && entry == 0) {
			it.forEach {
				if (answer.contains(it)) {
					answer_new.add(it)
				}
			}
			answer.clear()
			answer.addAll(answer_new)
			answer_new.clear()
		} else if (it == "") {
			count = count + answer.distinct().size
			answer.clear()
			entry = 1
		}
	}
	return count
}
// end::group_answers_2[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var solution1 = group_answers()
// end::part_1[]

// tag::part_2[]
	var solution2 = group_answers_2()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("*****************************")
	println("--- Day 6: Custom Customs ---")
	println("*****************************")
	println("Solution for part1")
	println("   $solution1 is the sum of those counts")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the sum of those counts")
	println()
// end::output[]
//}	