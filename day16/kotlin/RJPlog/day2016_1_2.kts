import java.io.File

// tag::ticket_2[]
fun ticket_2(): Long {
	var range = mutableMapOf<Int, String>()
	var range_count: Int = 0
	var rangeend: Boolean = false
	var nearticket: Boolean = false
	var yourticket: Boolean = false
	var yours = mutableListOf<Int>()
	var result: Long = 1
	var valueoutofrange: Int = 0
	var tickets = mutableListOf<String>()
	var tickets_new = mutableListOf<String>()
	var fields = mutableListOf<String>()
	var ticketnotvalid: Boolean

	// tag::read_puzzle[]
	File("day2016_puzzle_input.txt").forEachLine {
		if (it.contains('-') && !rangeend) {
			var instruction = it.split(":")
			var ranges = instruction[1].split(" or ")
			fields.add(instruction[0])
			range.put(range_count, ranges[0].replace(" ", "") + "-" + ranges[1].replace(" ", ""))
			range_count++
		} else if (it.contains("your")) {
			rangeend = true
			yourticket = true
		} else if (yourticket == true) {
			yourticket = false
			var hilf = it.split(",")
			hilf.forEach {
				yours.add(it.toInt())
			}
		} else if (it.contains("nearby")) {
			nearticket = true
		} else if (nearticket) {
			ticketnotvalid = false
			var singleTicket = it
			var fields_2 = it.split(",")
			fields_2.forEach {
				var value = it.toInt()
				range.forEach {
					var boundarys = it.value.split("-")
					if ((value < boundarys[0].toInt() || value > boundarys[1].toInt()) && (value < boundarys[2].toInt() || value > boundarys[3].toInt())) {
						valueoutofrange++
					}
				}
				if (valueoutofrange == range.size) {
					ticketnotvalid = true
				}
				valueoutofrange = 0
			}
			if (!ticketnotvalid) {
				tickets.add(singleTicket)
			}
		}
	}

	var boundary_count: Int
	var boundary_set: Int
	var boundary_set_m: Int
	var boundary_exceeded: Boolean
	var part_result: Int = 0
	var delete_key1: Int = -1
	var delete_entry: Int = -1

	while (range.size > 0) {
		for (m in 0..range.size - 1) {
			boundary_count = 0
			boundary_set = 0
			boundary_set_m = 0
			range.forEach {
				var boundarys_1 = it.value.split("-")
				boundary_exceeded = false
				tickets.forEach {
					var values = it.split(",")
					var value = values[m].toInt()
					if (value < boundarys_1[0].toInt() || value > boundarys_1[1].toInt() && value < boundarys_1[2].toInt() || value > boundarys_1[3].toInt()) {
						boundary_count++
						boundary_exceeded = true
					}
				}
				if (!boundary_exceeded) {
					boundary_set = it.key
					boundary_set_m = m
					part_result = yours.get(boundary_set_m)
				}
			}
			if (boundary_count == range.size - 1) {
				if (fields.get(boundary_set).contains("departure")) {
					result = result * part_result.toLong()
				}
				delete_key1 = boundary_set
				delete_entry = boundary_set_m
			}
		}
		range.remove(delete_key1)
		tickets.forEach {
			var new_ticket = ""
			var entry = it.split(",")
			for (z in 0..entry.size - 1) {
				if (z != delete_entry) {
					new_ticket = new_ticket + entry[z] + ","
				}
			}
			tickets_new.add(new_ticket.dropLast(1))
		}
		yours.removeAt(delete_entry)
		tickets = tickets_new
		tickets_new = mutableListOf()
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
	var t2 = System.currentTimeMillis()
	var solution2 = ticket_2()
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
	println()
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
	println("****************************")
	println("Solution for part2")
	println("   $solution2")
	println()
// end::output[]
//}	