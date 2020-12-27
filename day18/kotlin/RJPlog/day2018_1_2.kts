import java.io.File

// tag::new_math_2[]
fun new_math_2(): Long {
	var term = mutableListOf<String>()
	var overall_result: Long = 0

	// read file into list 'term'
	File("day2018_puzzle_input.txt").forEachLine {
		term.add(it)
	}

	// calculate result of each term
	term.forEach {
		var equation = it
		var close_index: Int = -1
		var part_term: String
		var open_index: Int = -1
		var result: Long = 0
		var term_result: Long = 1

		// strip term down to parts without brackets, calculate result of that part
		// replace the bracket expression with the result in the original string
		// do until all bracket expressions are resolved
		while (true) {
			
			// find bracket expression, assign it to 'part_term'
			if (equation.contains(')')) {
				close_index = equation.indexOf(')')
				part_term = equation.take(equation.indexOf(')'))
				open_index = part_term.lastIndexOf('(')
				part_term = part_term.drop(part_term.lastIndexOf('(') + 1)
			} else {
				part_term = equation
			}

			// split 'part_term' into sum operations
			var add_term = part_term.split(" * ")

			// calculate result for each sum operations, multiply all results and assign value to 'term_result'		
			add_term.forEach {
				var summand = it.split(" + ")
				summand.forEach {
					result = result + it.toLong()
				}
				term_result = term_result * result
				result = 0
			}

			// replace bracket expression with term_result for next turn or break and sum up overall result
			if (equation.contains(')')) {
				equation = equation.replaceRange(open_index, close_index + 1, term_result.toString())
				term_result = 1
			} else {
				overall_result = overall_result + term_result
				break
			}
		}
	}
	return overall_result
}
// end::new_math_2[]


// tag::new_math[]
fun new_math(): Long {
	var term = mutableListOf<String>()
	var overall_result: Long = 0

	// read file into list 'term'
	File("day2018_puzzle_input.txt").forEachLine {
		term.add(it)
	}

	// calculate result of each term
	term.forEach {
		var equation = it
		var close_index: Int = -1
		var part_term: String
		var open_index: Int = -1
		var result: Long

		// strip term down to parts without brackets, calculate result of that part
		// replace the bracket expression with the result in the original string
		// do until all bracket expressions are resolved
		while (true) {
			
			// find bracket expression, assign it to 'part_term'
			if (equation.contains(')')) {
				close_index = equation.indexOf(')')
				part_term = equation.take(equation.indexOf(')'))
				open_index = part_term.lastIndexOf('(')
				part_term = part_term.drop(part_term.lastIndexOf('(') + 1)
			} else {
				part_term = equation
			}

			// split part_term into values and operators, go through step by step and add/mul up the result
			var calc_term = part_term.split(" ")
			result = calc_term[0].toLong()
			for (i in 2..calc_term.size - 1 step 2) {
				if (calc_term[i - 1].equals("+")) {
					result = result + calc_term[i].toLong()
				} else if (calc_term[i - 1].equals("*")) {
					result = result * calc_term[i].toLong()
				}
			}

			// replace bracket expression with term_result for next turn or break and sum up overall result
			if (equation.contains(')')) {
				equation = equation.replaceRange(open_index, close_index + 1, result.toString())
			} else {
				overall_result = overall_result + result.toLong()
				break
			}
		}
	}
	return overall_result
}
// end::new_math[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = new_math()
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = new_math_2()
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("*******************************")
	println("--- Day 18: Operation Order ---")
	println("*******************************")
	println("Solution for part1")
	println("   $solution1 is the sum of the resulting values")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the sum of the resulting values using the new rules")
	println()
// end::output[]
//}	