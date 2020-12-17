import java.io.File

// tag::grid_2[]
fun grid_2(): Int {

	data class Quadruple<out A, out B, out C, out D>(
		val first: A,
		val second: B,
		val third: C,
		val fourth: D
	)

	val Grid = mutableMapOf<Quadruple<Int, Int, Int, Int>, Char>()
	val Grid_new = mutableMapOf<Quadruple<Int, Int, Int, Int>, Char>()
	var x: Int = 0
	var y: Int = 0
	var z: Int = 0
	var w: Int = 0

	File("day2017_puzzle_input.txt").forEachLine {
		it.forEach {
			Grid.put(Quadruple(x, y, z, w), it)
			x++
		}
		y++
		x = 0
	}

	//  directions for applying rules
	var dlts = mutableListOf<Quadruple<Int, Int, Int, Int>>()
	for (xx in -1..1) {
		for (yy in -1..1) {
			for (zz in -1..1) {
				for (ww in -1..1) {
					dlts.add(Quadruple(xx, yy, zz, ww))
				}
			}
		}
	}

	dlts.remove(Quadruple(0, 0, 0, 0))

	var sum: Int

	for (i in 0..5) {  // repeat 6 times
		// extend grid by add additional layer
		Grid_new.putAll(Grid)
		Grid.forEach {
			var xpos = it.key.first
			var ypos = it.key.second
			var zpos = it.key.third
			var wpos = it.key.fourth
			for (dlt in dlts) {
				var (dx, dy, dz, dw) = dlt
				if (!Grid.containsKey(Quadruple(xpos + dx, ypos + dy, zpos + dz, wpos + dw))) {
					Grid_new.put(Quadruple(xpos + dx, ypos + dy, zpos + dz, wpos + dw), '.')
				}
			}
		}
		Grid.clear()
		Grid.putAll(Grid_new)
		Grid_new.clear()

		Grid.forEach {
			// apply rules
			var texture = it.value
			var xpos = it.key.first
			var ypos = it.key.second
			var zpos = it.key.third
			var wpos = it.key.fourth
			sum = 0
			for (dlt in dlts) {
				var (dx, dy, dz, dw) = dlt
				if (Grid.getOrDefault(Quadruple(xpos + dx, ypos + dy, zpos + dz, wpos + dw), '0') == '#') {
					sum++
				}
			}
			if (texture == '#' && (sum == 2 || sum == 3)) {
				Grid_new.put(it.key, '#')
			} else if (texture == '.' && sum == 3) {
				Grid_new.put(it.key, '#')
			} else {
				Grid_new.put(it.key, '.')
			}
		}
		Grid.clear()
		Grid.putAll(Grid_new)
		Grid_new.clear()
	}    // repeat 6 times

	return Grid.filter { it.value == '#' }.count()
}
// end::grid_2[]

// tag::grid[]
fun grid(): Int {
	val Grid = mutableMapOf<Triple<Int, Int, Int>, Char>()
	val Grid_new = mutableMapOf<Triple<Int, Int, Int>, Char>()
	var x: Int = 0
	var y: Int = 0
	var z: Int = 0

	File("day2017_puzzle_input.txt").forEachLine {
		it.forEach {
			Grid.put(Triple(x, y, z), it)
			x++
		}
		y++
		x = 0
	}

	//  directions for applying rules
	var dlts = mutableListOf<Triple<Int, Int, Int>>()
	for (xx in -1..1) {
		for (yy in -1..1) {
			for (zz in -1..1) {
				dlts.add(Triple(xx, yy, zz))

			}
		}
	}
	dlts.remove(Triple(0, 0, 0))

	var sum: Int

	for (i in 0..5) {  // repeat 6 times

		// extend grid by add additional layer
		Grid_new.putAll(Grid)
		Grid.forEach {
			var xpos = it.key.first
			var ypos = it.key.second
			var zpos = it.key.third
			for (dlt in dlts) {
				var (dx, dy, dz) = dlt
				if (!Grid.containsKey(Triple(xpos + dx, ypos + dy, zpos + dz))) {
					Grid_new.put(Triple(xpos + dx, ypos + dy, zpos + dz), '.')
				}
			}
		}
		Grid.clear()
		Grid.putAll(Grid_new)
		Grid_new.clear()

		Grid.forEach {
			// apply rules
			var texture = it.value
			var xpos = it.key.first
			var ypos = it.key.second
			var zpos = it.key.third
			sum = 0
			for (dlt in dlts) {
				var (dx, dy, dz) = dlt
				if (Grid.getOrDefault(Triple(xpos + dx, ypos + dy, zpos + dz), '0') == '#') {
					sum++
				}
			}
			if (texture == '#' && (sum == 2 || sum == 3)) {
				Grid_new.put(it.key, '#')
			} else if (texture == '.' && sum == 3) {
				Grid_new.put(it.key, '#')
			} else {
				Grid_new.put(it.key, '.')
			}
		}
		Grid.clear()
		Grid.putAll(Grid_new)
		Grid_new.clear()
	}    // repeat 6 times

	return Grid.filter { it.value == '#' }.count()
}
// end::grid[]

//fun main(args: Array<String>) {
// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = grid()
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = grid_2()
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
	println()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("****************************")
	println("--- Day 17: Conway Cubes ---")
	println("****************************")
	println("Solution for part1")
	println("   $solution1 cubes are left in the active state after the sixth cycle")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 cubes are left in the active state after the sixth cycle")
	println()
// end::output[]
//}	