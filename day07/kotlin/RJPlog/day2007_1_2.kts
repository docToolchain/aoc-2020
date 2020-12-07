import java.io.File

// tag::shiny_bag[]
fun shiny_bag(): Int {
	var count: Int = 0
	var gameend: Boolean = false
	var rules = mutableListOf<String>()
	var bags = mutableListOf<String>()
	var bags_new = mutableListOf<String>()

	bags.add("shiny gold")

	File("day2007_puzzle_input.txt").forEachLine {
		if (it.take(10) != "shiny gold") {
			rules.add(it)
		}
	}

	while (!gameend) {
		rules.forEach {
			var instruction = it.split("contain")
			bags.forEach {
				if (instruction[1].contains(it.toString())) {
					bags_new.add(instruction[0].dropLast(2))
				}
			}
		}

		count = bags.size
		bags_new.forEach {
			if (!bags.contains(it)) {
				bags.add(it)
			}
		}
		
		bags_new.clear()
		if (bags.size == count) {
			gameend = true
		}
	}
	return count - 1
}
// end::shiny_bag[]

// tag::shiny_bag_2[]
fun shiny_bag_2(start: String): Int {
	var count: Int = 0
	var rules = mutableListOf<String>()

	File("day2007_puzzle_input.txt").forEachLine {
		rules.add(it)
	}

	rules.forEach {
		var instruction = it.split(" contain ")

		if (instruction[0].contains(start) && instruction[1].contains("no other bags")) {
			return 1
		} else if (instruction[0].contains(start)) {
			var content = instruction[1].split(", ")
			content.forEach {
				var number = it.take(1).toInt()
				var container = it.drop(2).dropLast(2)
				count = count + number * shiny_bag_2(container)
			}
			count = count + 1
			return count
		}
	}
	return count
}
// end::shiny_bag_2[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var solution1 = shiny_bag()
// end::part_1[]

// tag::part_2[]
	var solution2 = shiny_bag_2("shiny gold") - 1
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("******************************")
	println("--- Day 7: Handy Haversacks---")
	println("******************************")
	println("Solution for part1")
	println("   $solution1 bag colors can eventually contain at least one shiny gold bag")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 individual bags are required inside your single shiny gold bag")
	println()
// end::output[]
//}