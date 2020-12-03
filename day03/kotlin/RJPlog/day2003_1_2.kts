import java.io.File

//tag::identify_wood_width[]
fun WidthGrid2003(): Int {
	var width: Int = 0
	File("day2003_puzzle_input.txt").forEachLine { width = it.length }
	return width
}
//end::identify_wood_width[]

//tag::identify_wood_depth[]
fun DepthGrid2003(): Int {
	var depth: Int = 0
	File("day2003_puzzle_input.txt").forEachLine { depth = depth + 1 }
	return depth
}
//end::identify_wood_depth[]

//tag::setup_wood_grid[]
fun SetupGrid2003(): MutableMap<String, String> {
	val Grid = mutableMapOf<String, String>()
	var Position: String
	var Texture: String
	var ypos: Int = 0

	File("day2003_puzzle_input.txt").forEachLine {
		for (xpos in 0..it.length - 1) {
			Position = (xpos).toString() + "=" + ypos.toString()
			Texture = it[xpos].toString()
			Grid.put(Position, Texture)
		}
		ypos = ypos + 1
	}
	return Grid
}
//end::setup_wood_grid[]

//tag::toboggan_wood_grid[]
fun WalkGrid2003(Grid_input: MutableMap<String, String>, width: Int, depth: Int, xstep: Int, ystep: Int): Int {
	var solution: Int = 0
	var x: Int = 0
	var y: Int = 0
	var Grid = Grid_input

	while (y < depth) {
		if (Grid.getValue(x.toString() + "=" + y.toString()) == "#") {
			solution++
		}
		x = (x + xstep).rem(width)
		y = y + ystep
	}
	return solution
}
//end::toboggan_wood_grid[]

//fun main(args: Array<String>) {
	var solution1: Int
	var solution2: Long = 1
	var xstep: Int 
	var ystep: Int 

//tag::read_puzzle[]
	var width = WidthGrid2003()    
	var depth = DepthGrid2003()
	var Grid_Init = SetupGrid2003()
//end::read_puzzle[]

// tag::part_1[]
	xstep = 3
	ystep = 1
	solution1 = WalkGrid2003(Grid_Init, width, depth, xstep, ystep)
// end::part_1[]

// tag::part_2[]
	xstep = 1
	ystep = 1
	solution2 = solution2 * WalkGrid2003(Grid_Init, width, depth, xstep, ystep)
	xstep = 3
	ystep = 1
	solution2 = solution2 * WalkGrid2003(Grid_Init, width, depth, xstep, ystep)
	xstep = 5
	ystep = 1
	solution2 = solution2 * WalkGrid2003(Grid_Init, width, depth, xstep, ystep)
	xstep = 7
	ystep = 1
	solution2 = solution2 * WalkGrid2003(Grid_Init, width, depth, xstep, ystep)
	xstep = 1
	ystep = 2
	solution2 = solution2 * WalkGrid2003(Grid_Init, width, depth, xstep, ystep)
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("****************************")
	println("--- Day 3: Toboggan Trajectory ---")
	println("****************************")
	println("Solution for part1")
	println("   $solution1 trees would you encounter")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2")
	println()
// end::output[]
//}