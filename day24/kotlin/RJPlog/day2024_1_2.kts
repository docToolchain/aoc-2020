import java.io.File

// tag::lobby_layout_2[]
fun lobby_layout_2(input: MutableMap<Pair<Double, Double>, Int>): Int {

	// get prepared puzzle input
	var Grid = input
	var Grid_new = mutableMapOf<Pair<Double, Double>, Int>()

	Grid.forEach {
		if (it.value % 2 != 0) {
			Grid.put(it.key, 1)
		} else {
			Grid.put(it.key, 0)
		}
	}

	// directions
	var dlts = listOf(
		Pair(0.0, 1.0), // w
		Pair(1.0, 0.5), // nw
		Pair(1.0, -0.5), // ne
		Pair(0.0, -1.0), // e
		Pair(-1.0, -0.5), // se
		Pair(-1.0, 0.5) // sw
	)

	var sum: Int

	for (i in 1..100) {  // repeat 100 times

		// extend Grid by add additional layer
		Grid_new.putAll(Grid)
		Grid.forEach {
			var xpos = it.key.first
			var ypos = it.key.second
			for (dlt in dlts) {
				var (dx, dy) = dlt
				if (!Grid.containsKey(Pair(xpos + dx, ypos + dy))) {
					Grid_new.put(Pair(xpos + dx, ypos + dy), 0)
				}
			}
		}

		Grid = Grid_new
		Grid_new = mutableMapOf()

		// apply rules for changing tiles and store in a new grid
		Grid.forEach {
			var texture = it.value
			var xpos = it.key.first
			var ypos = it.key.second
			sum = 0
			for (dlt in dlts) {
				var (dx, dy) = dlt
				if (Grid.getOrDefault(Pair(xpos + dx, ypos + dy), -1) == 1) {
					sum++
				}
			}
			if (texture == 1 && (sum == 0 || sum > 2)) {
				Grid_new.put(it.key, 0)
			} else if (texture == 0 && sum == 2) {
				Grid_new.put(it.key, 1)
			} else {
				Grid_new.put(it.key, it.value)
			}
		}

		// replace old grid with new grid for next run
		Grid = Grid_new
		Grid_new = mutableMapOf()

	} // repeat 100 times

	// count black tiles
	return Grid.filter { it.value == 1 }.count()
}
// end::lobby_layout_2[]


// tag::lobby_layout[]
fun lobby_layout(input: MutableMap<Pair<Double, Double>, Int>): Int {

	// get prepared puzzle input
	var Grid = input

	// if grid has an even value, tile is white
	// if grid has an uneven value, tile is black, so we have to count the uneven one's


	return Grid.filter { it.value % 2 != 0 }.count()
}
// end::lobby_layout[]

// tag::read_puzzle_input_24[]
fun read_puzzle_input_24(): MutableMap<Pair<Double, Double>, Int> {

	// puzzle_input should be stored in a map, first element of map is a pair of coordinates
	//
	//                         __ w:  y++1
	//    sw: y++0.5, x--1    /  \   nw: y++0.5, x++1
	//    se: y--0.5, x--1    \__/   ne: y--0.5, x++1
	//                            e:  y--1
	//
	//

	var Grid = mutableMapOf<Pair<Double, Double>, Int>()

	File("day2024_puzzle_input.txt").forEachLine {
		var puzzle_input = it
		var drop: Int = 0
		var xpos: Double = 0.0
		var ypos: Double = 0.0

		while (puzzle_input.length > 0) {
			if (puzzle_input[0].equals('n') && puzzle_input[1].equals('w')) {
				ypos = ypos + 0.5
				xpos = xpos + 1.0
				drop = 2
			} else if (puzzle_input[0].equals('n') && puzzle_input[1].equals('e')) {
				ypos = ypos - 0.5
				xpos = xpos + 1.0
				drop = 2
			} else if (puzzle_input[0].equals('s') && puzzle_input[1].equals('w')) {
				ypos = ypos + 0.5
				xpos = xpos - 1.0
				drop = 2
			} else if (puzzle_input[0].equals('s') && puzzle_input[1].equals('e')) {
				ypos = ypos - 0.5
				xpos = xpos - 1.0
				drop = 2
			} else if (puzzle_input[0].equals('w')) {
				ypos = ypos + 1.0
				drop = 1
			} else if (puzzle_input[0].equals('e')) {
				ypos = ypos - 1.0
				drop = 1
			}
			puzzle_input = puzzle_input.drop(drop)
		}
		// if position is reached before, increase value, if not put 1
		if (Grid.contains(Pair(xpos, ypos))) {
			Grid.put(Pair(xpos, ypos), Grid.getValue(Pair(xpos, ypos)) + 1)
		} else {
			Grid.put(Pair(xpos, ypos), 1)
		}
	}
	return Grid
}
// end::read_puzzle_input_24[]


//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = lobby_layout(read_puzzle_input_24())
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = lobby_layout_2(read_puzzle_input_24())
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
	println()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("***************************")
	println("--- Day24: Lobby Layout ---")
	println("***************************")
	println("Solution for part1")
	println("   $solution1 tiles are left with the black side up")
	println()
// print solution for part 2
	println("********************")
	println("Solution for part2")
	println("   $solution2 tiles will be black after 100 days")
	println()
// end::output[]
//}	