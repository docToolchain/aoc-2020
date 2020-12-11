import java.io.File

// tag::create_seat_plan_2[]
fun seats_occupied_2(): Int {
	var Grid = mutableMapOf<String, String>()
	var x: Int = 0
	var y: Int = 0

	File("day2011_puzzle_input.txt").forEachLine {
		it.forEach {
			Grid.put(x.toString() + "=" + y.toString(), it.toString())
			x++
		}
		y++
		x = 0
	}

	var sum: Int
	var Grid_new = mutableMapOf<String, String>()
	var gameend: Boolean = false
	var count: Int = 0

	while (!gameend) {
		gameend = true
		Grid.forEach {
			var texture = it.value
			var position = it.key.split("=")
			var xpos = position[0].toInt()
			var ypos = position[1].toInt()
			var xoff = 1
			var yoff = 1
			var cond1_vis: Boolean = false
			var cond2_vis: Boolean = false
			var cond3_vis: Boolean = false
			var cond4_vis: Boolean = false
			var cond5_vis: Boolean = false
			var cond6_vis: Boolean = false
			var cond7_vis: Boolean = false
			var cond8_vis: Boolean = false
			sum = 0

			// tag::determine_status_next_visible_seat[]
			// direction up
			while (Grid.getOrDefault((xpos).toString() + "=" + (ypos - yoff).toString(), "0").equals(".")) {
				yoff++
			}
			if (Grid.getOrDefault((xpos).toString() + "=" + (ypos - yoff).toString(), "0").equals("#")) {
				cond1_vis = true
				sum++
			}
			yoff = 1
			// direction up-rigth
			while (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals(".")) {
				yoff++
				xoff++
			}
			if (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals("#")) {
				cond2_vis = true
				sum++
			}
			yoff = 1
			xoff = 1
			// direction rigth
			while (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos).toString(), "0").equals(".")) {
				xoff++
			}
			if (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos).toString(), "0").equals("#")) {
				cond3_vis = true
				sum++
			}
			xoff = 1
			// direction rigth-down
			while (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals(".")) {
				yoff++
				xoff++
			}
			if (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals("#")) {
				cond4_vis = true
				sum++
			}
			yoff = 1
			xoff = 1
			// direction down
			while (Grid.getOrDefault((xpos).toString() + "=" + (ypos + yoff).toString(), "0").equals(".")) {
				yoff++
			}
			if (Grid.getOrDefault((xpos).toString() + "=" + (ypos + yoff).toString(), "0").equals("#")) {
				cond5_vis = true
				sum++
			}
			yoff = 1
			// direction down-left
			while (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals(".")) {
				yoff++
				xoff++
			}
			if (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals("#")) {
				cond6_vis = true
				sum++
			}
			yoff = 1
			xoff = 1
			// direction left
			while (Grid.getOrDefault((xpos-xoff).toString() + "=" + (ypos).toString(), "0").equals(".")) {
				xoff++
			}
			if (Grid.getOrDefault((xpos-xoff).toString() + "=" + (ypos).toString(), "0").equals("#")) {
				cond7_vis = true
				sum++
			}
			xoff = 1
						// direction up-left
			while (Grid.getOrDefault((xpos-xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals(".")) {
				yoff++
				xoff++
			}
			if (Grid.getOrDefault((xpos-xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals("#")) {
				cond8_vis = true
				sum++
			}
			// end::determine_status_next_visible_seat[]

			if (texture.equals("L")) {
				if (!cond1_vis && !cond2_vis && !cond3_vis && !cond4_vis && !cond5_vis && !cond6_vis && !cond7_vis && !cond8_vis) {
					Grid_new.put(it.key, "#")
					gameend = false
				} else {
					Grid_new.put(it.key, "L")
				}
			} else if (texture.equals("#")) {
				if (sum > 4) {
					Grid_new.put(it.key, "L")
					gameend = false
				} else {
					Grid_new.put(it.key, "#")
				}

			} else {
				Grid_new.put(it.key, ".")
			}
		}
		Grid.clear()
		Grid.putAll(Grid_new)
		Grid_new.clear()
	} // gameend

	Grid.forEach {
		if (it.value.equals("#")) {
			count++
		}
	}
	return count
}
// end::create_seat_plan_2[]

// tag::create_seat_plan[]
fun seats_occupied(): Int {
	var Grid = mutableMapOf<Pair<Int, Int>, String>()
	var x: Int = 0
	var y: Int = 0

	File("day2011_puzzle_input.txt").forEachLine {
		it.forEach {
			Grid.put(Pair(x,y), it.toString())
			x++
		}
		y++
		x = 0
	}

	var sum: Int
	var Grid_new = mutableMapOf<Pair<Int, Int>, String>()
	var gameend: Boolean = false
	var count: Int = 0

	while (!gameend) {
		gameend = true
		Grid.forEach {
			var texture = it.value
			var xpos = it.key.first
			var ypos = it.key.second

			var cond1: Boolean
			var cond2: Boolean
			var cond3: Boolean
			sum = 0

			if (texture.equals("L")) {
				cond1 = !Grid.getOrDefault(Pair(xpos - 1,ypos - 1),".").equals("#") && !Grid.getOrDefault(Pair(xpos,ypos - 1), ".").equals("#") && !Grid.getOrDefault(Pair(xpos + 1,ypos - 1), ".").equals("#")
				cond2 = !Grid.getOrDefault(Pair(xpos - 1,ypos),".").equals("#") && !Grid.getOrDefault(Pair(xpos + 1,ypos), ".").equals("#")
				cond3 = !Grid.getOrDefault(Pair(xpos - 1,ypos + 1),".").equals("#") && !Grid.getOrDefault(Pair(xpos,ypos + 1), ".").equals("#") && !Grid.getOrDefault(Pair(xpos + 1,ypos + 1), ".").equals("#")
				if (cond1 && cond2 && cond3) {
					Grid_new.put(it.key, "#")
					gameend = false
				} else {
					Grid_new.put(it.key, "L")
				}
			} else if (texture.equals("#")) {
				if (Grid.getOrDefault(Pair(xpos - 1,ypos - 1), ".").equals("#")) {
					sum++
				}
				if (Grid.getOrDefault(Pair(xpos,ypos - 1), ".").equals("#")) {
					sum++
				}
				if (Grid.getOrDefault(Pair(xpos + 1,ypos - 1), ".").equals("#")) {
					sum++
				}
				if (Grid.getOrDefault(Pair(xpos - 1,ypos), ".").equals("#")) {
					sum++
				}
				if (Grid.getOrDefault(Pair(xpos + 1,ypos), ".").equals("#")) {
					sum++
				}
				if (Grid.getOrDefault(Pair(xpos - 1,ypos + 1), ".").equals("#")) {
					sum++
				}
				if (Grid.getOrDefault(Pair(xpos,ypos + 1), ".").equals("#")) {
					sum++
				}
				if (Grid.getOrDefault(Pair(xpos + 1,ypos + 1), ".").equals("#")) {
					sum++
				}
				if (sum > 3) {
					Grid_new.put(it.key, "L")
					gameend = false
				} else {
					Grid_new.put(it.key, "#")
				}
			} else {
				Grid_new.put(it.key, ".")
			}
		}
		Grid.clear()
		Grid.putAll(Grid_new)
		Grid_new.clear()
	}

	Grid.forEach {
		if (it.value.equals("#")) {
			count++
		}
	}
	return count
}
// end::create_seat_plan[]


//fun main(args: Array<String>) {

// tag::part_1[]
	var solution1 = seats_occupied()
// end::part_1[]

// tag::part_2[]
	var solution2 = seats_occupied_2()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("****************************")
	println("--- Day 11: Seating System ---")
	println("****************************")
	println("Solution for part1")
	println("   $solution1 seats end up occupied")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 any seats end up occupied")
	println()
// end::output[]
//}	