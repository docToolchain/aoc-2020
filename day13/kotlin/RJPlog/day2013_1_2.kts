import java.io.File

// tag::bus_2[]
fun bus_2(): Long {
	var departure = mutableListOf<Pair<Long, Long>>()
	var firstline: Boolean = true
	var count: Long = 0
	File("day2013_puzzle_input.txt").forEachLine {
		if (firstline) {
			firstline = false
		} else {
			var instruction = it.split(",")
			instruction.forEach {
				if (!it.equals("x")) {
					departure.add(Pair(count, it.toLong()))
				}
				count++
			}
		}
	}

	var timestamp: Long = 0 
	var step_size: Long = 1
	var step_size_index: Int = 1
	var freq1: Long = 0
	var search_freq1: Boolean = false
	var sum: Int = 1
	var k: Long = 0

	while (true) {
		departure.forEach {
			if ((timestamp + it.first) % (it.second) > 0) {
				sum++
			}
		}
		// calc step_size  --> step_size one will take to long
		var a = departure[0]
		var b = departure[step_size_index]
		if ((timestamp + a.first) % (a.second) < 1 && (timestamp + b.first) % (b.second) < 1) {
			if (!search_freq1) {
				freq1 = timestamp
				search_freq1 = true
			} else {
				step_size = timestamp - freq1
				search_freq1 = false
				step_size_index++
			}
		}
		println(step_size)  // here you can se the result of the dynamic step_size approach
		if (sum < 1) {
			println("number of steps: $k")
			return timestamp
		}
		sum = 0
		timestamp = timestamp + step_size
		k++
	}
}
// end::bus_2[]


// tag::bus[]
fun bus(): Long {
	var departure = mutableListOf<Long>()
	var firstline: Boolean = true
	var dep_time: Long = 0
	File("day2013_puzzle_input.txt").forEachLine {
		if (firstline) {
			dep_time = it.toLong()
			firstline = false
		} else {
			var instruction = it.split(",")
			instruction.forEach {
				if (!it.equals("x")) {
					departure.add(it.toLong())
				}
			}
		}
	}

	var early_bus: Long = 10000
	var result: Long = 0
	departure.forEach {
		if ((it - dep_time % it) < early_bus) {
			early_bus = it - dep_time % it
			result = it * (it - dep_time % it)
		}
	}
	return result
}
// end::bus[]

//fun main(args: Array<String>) {
// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = bus()
	t1 = System.currentTimeMillis() - t1
	println()

// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = bus_2()
	t2 = System.currentTimeMillis() - t2

	println()
	println("part 1 solved in $t1 ms -> $solution1")
	println()
	println("part 2 solved in $t2 ms -> $solution2")
	println()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("****************************")
	println("--- Day 13: Shuttle Search ---")
	println("****************************")
	println("Solution for part1")
	println("   $solution1 is the ID of the earliest bus you can take to the airport multiplied by the number of minutes")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list")
	println()
// end::output[]
//}	