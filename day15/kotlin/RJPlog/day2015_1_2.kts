import java.io.File

// tag::elves_game_rework_3[]
fun elves_game_3(): Int {
	var first = mutableMapOf<Int, Int>()
	var second = mutableMapOf<Int, Int>()
	var last_spoken: Int = 0
	var new_value: Int
	var turn: Int = 1
	
	File("day2015_puzzle_input.txt").forEachLine {
		var instruction = it.split(",")
		instruction.forEach {
			first.put(it.toInt(), turn)
			last_spoken = it.toInt()
			turn++
		}
	}

	while (true) {  //30.000.000
		if (!second.containsKey(last_spoken)) {
			new_value = 0
			if (first.containsKey(new_value)) {
				second.put(new_value, first.getValue(new_value))
			}
			first.put(new_value, turn)
			last_spoken = new_value
		} else {
			new_value = first.getValue(last_spoken) - second.getValue(last_spoken)
			if (first.containsKey(new_value)) {
				second.put(new_value, first.getValue(new_value))
			}
			first.put(new_value, turn)
			last_spoken = new_value
		}
		turn++
		if (turn > 30000000) {
			return last_spoken
		}
	}
}
// end::elves_game_rework_3[]

// tag::elves_game_rework_2[]
fun elves_game_2(): Int {
	var row = mutableListOf<Int>()
	var last_spoken: Int
	var new_value: Int 
	var turn: Int = 0
	
	File("day2015_puzzle_input.txt").forEachLine {
		var instruction = it.split(",")
		instruction.forEach {
			row.add(it.toInt())
			turn++
		}
	}

	while (true) {  //30.000.000
		last_spoken = row.last()
		if ((row.filter { it == last_spoken }.size) == 1) {
			row.add(0)
		} else {
			var j = row.size - 2
			while (row[j] != last_spoken) {
				j--
			}
			new_value = j.toInt() + 1
			row.add(turn - new_value)
		}
		turn++
		if (turn > 2019) {
			return row.last()
		}
	}
}
// end::elves_game_2[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = elves_game_2()
	t1 = System.currentTimeMillis() - t1
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = elves_game_3()
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("***************************************")
	println("--- Day 15: Rambunctious Recitation ---")
	println("***************************************")
	println("Solution for part1")
	println("   $solution1 will be the 2020th number spoken")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 will be the 30000000th number spoken")
	println()
// end::output[]
//}	