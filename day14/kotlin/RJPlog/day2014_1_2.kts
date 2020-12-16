import java.io.File

// tag::docking_2[]
fun docking_2(): Long {
	var mem = mutableMapOf<Long, Long>()
	var mask: String = ""
	var cur_mem: String
	var new_mem: String = ""
	var add_val: Long
	var mem_list = mutableListOf<String>()
	var mem_list_new = mutableListOf<String>()

	File("day2014_puzzle_input.txt").forEachLine {
		var instruction = it.split(" = ")
		
		if (instruction[0].equals("mask")) {
			mask = instruction[1]
		} else if (instruction[0].contains("mem")) {
			cur_mem = instruction[0].dropLast(1).drop(4).toLong().toString(2).padStart(36, '0')
			add_val = instruction[1].toLong()
			for (i in 0..mask.length - 1) {
				if (mask[i].equals('X')) {
					new_mem = new_mem + "X"
				} else if (mask[i].equals('0')) {
					new_mem = new_mem + cur_mem[i]
				} else if (mask[i].equals('1')) {
					new_mem = new_mem + "1"
				}
			}

			// create list with new_mem where all X are replaced by 0/1 step by step
			var gameend: Boolean = false
			mem_list.add(new_mem)
			while (!gameend) {
				mem_list.forEach {
					if (it.contains('X')) {
						mem_list_new.add(it.replaceFirst('X', '0'))
						mem_list_new.add(it.replaceFirst('X', '1'))
					} else {
						mem_list_new.add(it)
					}
				}
				if (mem_list.size == mem_list_new.size) {
					gameend = true
				}
				mem_list = mem_list_new
				mem_list_new = mutableListOf()
			}

			mem_list.forEach {
				mem.put(it.toLong(2), add_val)
			}
			mem_list = mutableListOf()
			new_mem = ""
		}
	}

	var result: Long = 0
	mem.forEach {
		result = result + it.value
	}
	return result
}
// end::docking_2[]


// tag::docking[]
fun docking(): Long {
	var mem = mutableMapOf<Long, Long>()  // storage for the memory
	var mask: String = ""                 // this variable will hold the mask
	var cur_mem: Long                     // this variable will hold the memory address
	var add_val: String                   // this variable will hold the value supposed to store before applying the mask
	var new_val: String = ""              // this variable will hold the value to store after applying the mask

	File("day2014_puzzle_input.txt").forEachLine {
		var instruction = it.split(" = ")
		
		if (instruction[0].equals("mask")) {
			mask = instruction[1]
		} else if (instruction[0].contains("mem")) {
			cur_mem = instruction[0].dropLast(1).drop(4).toLong()
			add_val = instruction[1].toLong().toString(2).padStart(36, '0')
			for (i in 0..mask.length - 1) {
				if (mask[i].equals('X')) {
					new_val = new_val + add_val[i]
				} else {
					new_val = new_val + mask[i]
				}
				mem.put(cur_mem.toLong(), new_val.toLong(2))
			}
			new_val = ""
		}
	}
	var result: Long = 0
	mem.forEach {
		result = result + it.value
	}
	return result
}
// end::docking[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = docking()
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = docking_2()
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
	println()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("****************************")
	println("--- Day 14: Docking Data ---")
	println("****************************")
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