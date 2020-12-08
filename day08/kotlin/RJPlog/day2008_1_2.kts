import java.io.File
import kotlin.math.*

// tag::boot_code[]
fun boot_code(ProgramCode: List<String>): String {
	var accu: Int = 0
	val Program_exe = mutableMapOf<Int, Int>()
	var ProgramCount: Int = 0
	var j: Int = 0

	// Part 1: Read ProgramCode
	ProgramCode.forEach {
		Program_exe.put(j, 0)
		j++
	}

	while (ProgramCount < ProgramCode.size) {
		val instruction = ProgramCode[ProgramCount].split(" ")

		if (instruction[0] == "nop") {
			if (Program_exe.getValue(ProgramCount) == 1) {
				return "infinite-" + accu.toString()
			}
			Program_exe.put(ProgramCount, Program_exe.getValue(ProgramCount) + 1)
			ProgramCount = ProgramCount + 1
		} else if (instruction[0] == "acc") {
			if (Program_exe.getValue(ProgramCount) == 1) {
				return "infinite-" + accu.toString()
			}
			Program_exe.put(ProgramCount, Program_exe.getValue(ProgramCount) + 1)
			accu = accu + instruction[1].toInt()
			ProgramCount = ProgramCount + 1
		} else if (instruction[0] == "jmp") {
			if (Program_exe.getValue(ProgramCount) == 1) {
				return "infinite-" + accu.toString()
			}
			Program_exe.put(ProgramCount, Program_exe.getValue(ProgramCount) + 1)
			ProgramCount = ProgramCount + instruction[1].toInt()
		}
	}
	return accu.toString()
}
// end::boot_code[]

//fun main(args: Array<String>) {

// tag::read_puzzle[]
	val ProgramCode = mutableListOf<String>()
	File("day2008_puzzle_input.txt").forEachLine {
		ProgramCode.add(it)
	}
// end::read_puzzle[]

// tag::part_1[]
	var solution1 = boot_code(ProgramCode)
// end::part_1[]

// tag::part_2[]
	var solution2: String
	var replace: Int = 0
    var replace_count: Int = 0
	
	do {
		solution2 = boot_code(ProgramCode)
		ProgramCode.clear()		
		File("day2008_puzzle_input.txt").forEachLine {
			if (it.contains("jmp") || it.contains("nop")) {
				if (replace_count == replace) {
					if (it.contains("jmp")) {
						ProgramCode.add(it.replace("jmp", "nop"))
					} else if (it.contains("nop")) {
						ProgramCode.add(it.replace("nop", "jmp"))
					}
				} else {
					ProgramCode.add(it)
				}
				replace_count++
			} else {
				ProgramCode.add(it) // entwickle Algritmus and x. auffindort die instruction zu ändern.
			}
		}
		replace++
		replace_count = 0
	} while (solution2.contains("infinite"))
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("*******************************")
	println("--- Day 8: Handheld Halting ---")
	println("*******************************")
	println("Solution for part1")
	println("   $solution1 is the value in the accumulator ")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the value of the accumulator after the program terminates")
	println()
// end::output[]
//}	