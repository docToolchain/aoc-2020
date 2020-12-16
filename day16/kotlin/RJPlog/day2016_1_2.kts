import java.io.File

// tag::ticket_2[]
fun ticket_2(): Int {
	var range = mutableMapOf<Int, String>()
	var range_count: Int = 0
	var rangeend: Boolean = false
	var nearticket: Boolean = false
	var result: Int = 0
	var valueoutofrange: Int = 0

	// tag::read_puzzle[]
	File("day2016_puzzle_input.txt").forEachLine {
		if (it.contains('-') && !rangeend) {
			var instruction = it.split(":")
			var ranges = instruction[1].split(" or ")
			range.put(range_count, ranges[0].replace(" ", ""))
			range_count++
			range.put(range_count, ranges[1].replace(" ", ""))
			range_count++
		} else if (it.contains("your")) {
			rangeend = true
		} else if (it.contains("nearby")) {
			nearticket = true
		} else if (nearticket) {
			var fields = it.split(",")
			fields.forEach {
				var value = it.toInt()
				range.forEach {
					var boundarys = it.value.split("-")
					if (value < boundarys[0].toInt() || value > boundarys[1].toInt()) {
						valueoutofrange++
					}
				}
				if (valueoutofrange == range.size) {
					result = result + value
				}
				valueoutofrange = 0
			}
		}
	}
	return result
}
// end::ticket_2[]

// tag::ticket[]
fun ticket(): Int {
	var range = mutableMapOf<Int, String>()
	var range_count: Int = 0
	var rangeend: Boolean = false
	var nearticket: Boolean = false
	var result: Int = 0
	var valueoutofrange: Int = 0

	// tag::read_puzzle[]
	File("day2016_puzzle_input.txt").forEachLine {
		if (it.contains('-') && !rangeend) {
			var instruction = it.split(":")
			var ranges = instruction[1].split(" or ")
			range.put(range_count, ranges[0].replace(" ", ""))
			range_count++
			range.put(range_count, ranges[1].replace(" ", ""))
			range_count++
		} else if (it.contains("your")) {
			rangeend = true
		} else if (it.contains("nearby")) {
			nearticket = true
		} else if (nearticket) {
			var fields = it.split(",")
			fields.forEach {
				var value = it.toInt()
				range.forEach {
					var boundarys = it.value.split("-")
					if (value < boundarys[0].toInt() || value > boundarys[1].toInt()) {
						valueoutofrange++
					}
				}
				if (valueoutofrange == range.size) {
					result = result + value
				}
				valueoutofrange = 0
			}
		}


	}
// end::read_puzzle[]

	println(range)
	println(rangeend)
	println(result)


	return result
}
// end::ticket[]

//fun main(args: Array<String>) {


// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = ticket()
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
//	var t2 = System.currentTimeMillis()
//	var solution2 = ticket_2()
//	t2 = System.currentTimeMillis() - t2
//	println()
//	println("part 2 solved in $t2 ms -> $solution2")
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("**********************************")
	println("--- Day 16: Ticket Translation ---")
	println("**********************************")
	println("Solution for part1")
	println("   $solution1 ")
	println()
// print solution for part 2
//	println("****************************")
//	println("Solution for part2")
//	println("   $solution2")
//	println()
// end::output[]
//}	