import java.io.File

// tag::seat_id[]
fun seat_id(): Int {
	var id: Int = 0

	File("day2005_puzzle_input.txt").forEachLine {
		if (it.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1").toInt(2) > id) {
			id = it.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1").toInt(2)
		}
	}
	return id
}
// end::seat_id[]

// tag::occupied_seats[]
fun occupied_seats(max: Int): Int {
	var id: Int
	var occ_seats = mutableListOf<Int>()

	File("day2005_puzzle_input.txt").forEachLine {
		occ_seats.add(it.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1").toInt(2))
	}
	id = max
	while (occ_seats.contains(id)) {
		id--
	}
	return id
}
// end::occupied_seats[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var solution1 = seat_id()
// end::part_1[]

// tag::part_2[]
	var solution2 = occupied_seats(solution1)
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("******************************")
	println("--- Day 5: Binary Boarding ---")
	println("******************************")
	println("Solution for part1")
	println("   $solution1 is the highest seat ID on a boarding pass")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the ID of your seat")
	println()
// end::output[]
//}