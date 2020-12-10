import java.io.File

// tag::XMAS[]
fun XMAS(): Long {
	val numbers = mutableListOf<Long>()
	var result: Long = 0

	File("day2009_puzzle_input.txt").forEachLine {
		numbers.add(it.toLong())
	}

	for (i in 25..numbers.size - 1) {
		var treffer: Boolean = false
		for (j in i - 25..i - 1) {
			for (k in i - 25..i - 1) {
				if (j != k && numbers[j] + numbers[k] == numbers[i]) {
					treffer = true
				}
			}
		}
		if (!treffer) {
			result = numbers[i]
			return result
		}
	}
	return result
}
// end::XMAS[]

// tag::XMAS_2[]
fun XMAS_2(xmas: Long): Long {
	val numbers = mutableListOf<Long>()
	val range = mutableListOf<Long>()

	File("day2009_puzzle_input.txt").forEachLine {
		numbers.add(it.toLong())
	}

	var i = 0
	var j = 0
	while (i < numbers.size) {
		range.add(numbers[i + j])
		if (range.sum() == xmas) {
            var min: Long = xmas
            var max: Long = 0
            range.forEach {
                if (it < min) {
                    min = it
                } else if ( it > max) {
                    max  = it
                }
            }
			return max + min
		} else if (range.sum() > xmas) {
			range.clear()
			i++
			j = i
		} else if (range.sum() < xmas) {
			j++
		}
	}
	return 0
}
// end::XMAS_2[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var solution1 = XMAS()
// end::part_1[]

// tag::part_2[]
	var solution2 = XMAS_2(solution1)
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("*****************************")
	println("--- Day 9: Encoding Error ---")
	println("*****************************")
	println("Solution for part1")
	println("   $solution1 is the first number that does not have this property")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the encryption weakness in your XMAS-encrypted list of numbers")
	println()
// end::output[]
//}	