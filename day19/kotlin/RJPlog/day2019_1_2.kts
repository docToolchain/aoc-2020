import java.io.File

// tag::monster_message_2[]
fun monster_message_2(): Int {

	// tag::read_puzzle[]
	var ruleset = mutableMapOf<String, String>()
	var segment: Int = 0
	var messages = mutableListOf<String>()
	File("day2019_puzzle_input.txt").forEachLine {
		if (it == "") {
			segment++
		} else {
			when (segment) {
				0 -> {
					var instruction = it.split(":")
					// add " " befor and after the string, this is done for easier replacement of rules
					// --> replacing 14 could lead to strange results when matching 114
					// --> better to search for _14_, this could do no harm to _114_
					ruleset.put(" " + instruction[0] + " ", instruction[1] + " ")
				}
				1 -> messages.add(it)
			}
		}
	}
	ruleset.put(" 8 ", " 42 | 42 8 ")
	ruleset.put(" 11 ", " 42 31 | 42 11 31 ")
	// end::read_puzzle[]

	//tag::pre_ruleset_check_mes[]
	var rulezero = ruleset.getValue(" 0 ")
	var rulezero_reg: String
	var gameend = false
	var result_old: Int = 0
	var result: Int = 0

	while (!gameend) {
		result = 0
		ruleset.forEach {
			if (rulezero.contains(it.key)) {
				rulezero = rulezero.replace(it.key, " ( " + it.value + " ) ")
			}
		}

		rulezero_reg = rulezero.replace(" ", "").replace("\"", "")

		val pattern = rulezero_reg.toRegex()

		messages.forEach {
			if (pattern.matches(it)) {
				result++
			}
		}
		if (result > 0 && result == result_old) {
			gameend = true
		}
		result_old = result
	}
	//end::pre_ruleset_check_mes[]

	return result
}
// end::monster_message_2[]

// tag::monster_message[]
fun monster_message(): Int {
	// tag::read_puzzle[]
	var ruleset = mutableMapOf<String, String>()
	var segment: Int = 0
	var messages = mutableListOf<String>()
	File("day2019_puzzle_input.txt").forEachLine {
		if (it == "") {
			segment++
		} else {
			when (segment) {
				0 -> {
					var instruction = it.split(":")
					ruleset.put(" " + instruction[0] + " ", instruction[1] + " ")
				}
				1 -> messages.add(it)
			}
		}
	}
	// end::read_puzzle[]

	//first strategie: extend ruleset to all possible variants, then check for each message, if it is contained in extended ruleset. If ruleset contains >> allowed messages as messages recived, this could fail
	//second strategie: create a regex, and check for each message, if pattern matches message  -> I never worked with regular expressions, but it seems worth to learn it now

	//tag::prepare_ruleset[]
	var rulezero = ruleset.getValue(" 0 ")
	var gameend = false
	while (!gameend) {
		gameend = true
		ruleset.forEach {
			if (rulezero.contains(it.key)) {
				gameend = false
				rulezero = rulezero.replace(it.key, " ( " + it.value + " ) ")
			}
		}
	}
	rulezero = rulezero.replace(" ", "").replace("\"", "")
	val pattern = rulezero.toRegex()
	//end::prepare_ruleset[]

	//tag::check_messages[]
	var result: Int = 0
	messages.forEach {
		if (pattern.matches(it)) {
			result++
		}
	}
	//end::check_messages[]

	return result
}
// end::monster_message[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = monster_message()
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = monster_message_2()
	t2 = System.currentTimeMillis() - t2
	println("part 2 solved in $t2 ms -> $solution2")
	println()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("********************************")
	println("--- Day 19: Monster Messages ---")
	println("********************************")
	println("Solution for part1")
	println("   $solution1 messages completely match rule 0")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 messages completely match rule 0")
	println()
// end::output[]
//}	