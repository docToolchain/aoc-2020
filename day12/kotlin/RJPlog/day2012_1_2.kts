import java.io.File
import kotlin.math.*

// tag::storm[]
fun storm(): Int {
	var x: Int = 0
	var y: Int = 0
	var D: Int = 1 // 0 = North, 1 = East, 2 = South, 3 = West
	var i: Int

	File("day2012_puzzle_input.txt").forEachLine {
		var instruction = it.take(1)
		var distance = it.drop(1).toInt()
		when (instruction) {
			"N" -> {
				y = y + distance
			}
			"S" -> {
				y = y - distance
			}
			"E" -> {
				x = x + distance
			}
			"W" -> {
				x = x - distance
			}
			"R" -> {
				i = 0
				while (i < distance) {
					D++
					if (D > 3) {
						D = 0
					}
					i = i + 90
				}
			}
			"L" -> {
				i = 0
				while (i < distance) {
					D--
					if (D < 0) {
						D = 3
					}
					i = i + 90
				}
			}
			"F" -> {
				if (D == 0) {
					y = y + distance
				} else if (D == 1) {
					x = x + distance
				} else if (D == 2) {
					y = y - distance
				} else if (D == 3) {
					x = x - distance
				}
			}

		}
	}
	return abs(x) + abs(y)
}
// end::storm[]

// tag::storm_2[]
fun storm_2(): Int {
	var x: Int = 0
	var y: Int = 0
	var i: Int
	var x_way: Int = 10
	var y_way: Int = 1

	File("day2012_puzzle_input.txt").forEachLine {
		var instruction = it.take(1)
		var distance = it.drop(1).toInt()
		when (instruction) {
			"N" -> {
				y_way = y_way + distance
			}
			"S" -> {
				y_way = y_way - distance
			}
			"E" -> {
				x_way = x_way + distance
			}
			"W" -> {
				x_way = x_way - distance
			}
			"R" -> {
				if (distance == 90) {
					i = y_way
					y_way = -x_way
					x_way = i
				} else if (distance == 180) {
					y_way = -y_way
					x_way = -x_way
				} else if (distance == 270) {
					i = y_way
					y_way = x_way
					x_way = -i
				} 
			}
			"L" -> {
				if (distance == 90) {
					i = y_way
					y_way = x_way
					x_way = -i
				} else if (distance == 180) {
					y_way = -y_way
					x_way = -x_way
				} else if (distance == 270) {
					i = y_way
					y_way = -x_way
					x_way = i
				} 
			}
			"F" -> {
				x = x + distance * x_way
				y = y + distance * y_way
			}
		}
	}
	return abs(x) + abs(y)
}
// end::storm_2[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = storm()
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = storm_2()
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
// end::part_2[]

// tag::output[]
// print solution for part 1
	println()
	println("****************************")
	println("--- Day 12: Rain Risk ---")
	println("****************************")
	println("Solution for part1")
	println("   $solution1 is the Manhattan distance between that location and the ship's starting position")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the Manhattan distance between that location and the ship's starting position")
	println()
// end::output[]
//}