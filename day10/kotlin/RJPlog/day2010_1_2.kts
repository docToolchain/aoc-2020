import java.io.File

// tag::jolts[]
fun jolts(): Int {
	var jolt_chain = mutableListOf<Int>(0)

	File("day2010_puzzle_input.txt").forEachLine {
		jolt_chain.add(it.toInt())
	}
	
	//jolt_chain.add(jolt_chain.max()!! + 3)
	var max: Int = 0
	jolt_chain.forEach {
		if (it > max) {
			max = it
		}
	}
	jolt_chain.add(max + 3)

	var jolt_chain_sorted = jolt_chain.sorted()
	var count_1: Int = 0
	var count_2: Int = 0

	for (i in 0..jolt_chain_sorted.size - 2) {
		if (jolt_chain_sorted[i + 1] - jolt_chain_sorted[i] == 1) {
			count_1++
		} else if (jolt_chain_sorted[i + 1] - jolt_chain_sorted[i] == 3) {
			count_2++
		}
	}
	return count_1 * count_2
}
// end::jolts[]

// tag::jolts_2[]
fun jolts_2(): Long {
	var jolt_chain = mutableListOf<Int>(0)
	var gameend: Boolean = false

	File("day2010_puzzle_input.txt").forEachLine {
		jolt_chain.add(it.toInt())
	}
	
	//jolt_chain.add(jolt_chain.max()!! + 3)
	var max: Int = 0
	jolt_chain.forEach {
		if (it > max) {
			max = it
		}
	}
	jolt_chain.add(max + 3)

	var jolt_chain_sorted = jolt_chain.sorted()
	var dist3 = mutableListOf<Int>()
	var pos_con = mutableListOf<String>("0")
	var pos_con_new = mutableListOf<String>()
	var result: Long = 1

	for (i in 0..jolt_chain_sorted.size - 2) {
		if (jolt_chain_sorted[i + 1] - jolt_chain_sorted[i] == 3) {
			dist3.add(jolt_chain_sorted[i + 1])
		}
	}

	for (j in 0..dist3.size - 1) {// calculate iterative starting from 0 to the next chain link with 3 jolts difference, then from there to the next 3 jolts difference and so on 
		var runend = dist3[j]

		while (!gameend) {
			gameend = true
			pos_con.forEach {
				var curr_chain = it
				var instruction = it.split("-")
				var last_joint = instruction[0].toInt()
				if (last_joint != runend) {
					gameend = false
					jolt_chain.forEach {
						if (it - last_joint < 4 && it - last_joint > 0) {
							pos_con_new.add(it.toString() + "-" + curr_chain)
						}
					}
				} else {
					pos_con_new.add(curr_chain)
				}
			}
			pos_con.clear()
			pos_con.addAll(pos_con_new)
			pos_con_new.clear()
		}

		result = result * pos_con.size
		pos_con.clear()
		pos_con.add(dist3[j].toString())
		gameend = false

	}
	return result
}
// end::jolts_2[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var solution1 = jolts()
// end::part_1[]

// tag::part_2[]
	var solution2 = jolts_2()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("*****************************")
	println("--- Day 10: Adapter Array ---")
	println("*****************************")
	println("Solution for part1")
	println("   $solution1 is the number of 1-jolt differences multiplied by the number of 3-jolt differences")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device")
	println()
// end::output[]
//}	