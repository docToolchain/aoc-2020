import java.io.File

//fun main(args: Array<String>) {
// tag::part_1[]
	var value: Long = 1
	val subject_number: Long = 7
	val card_public_key: Long = 1327981  // copy first line of puzzle_input
	val door_public_key: Long = 2822615  // copy second line of puzzle_input

	var j: Long = 0
	while (value != card_public_key) {
		value = value * subject_number % 20201227
		j++
	}
	var card_loop_size = j

	j = 0
	value = 1
	while (value != door_public_key) {
		value = value * subject_number % 20201227
		j++
	}
	var door_loop_size = j

	println("Card's loop size is $card_loop_size, door's loop size is $door_loop_size")

	value = 1
	for (i in 1..door_loop_size) {
		value = value * card_public_key % 20201227
	}
	print("Encryption Key is: $value,  ")
	value = 1
	for (i in 1..card_loop_size) {
		value = value * door_public_key % 20201227
	}
	println(value)

	var t1 = System.currentTimeMillis()
	var solution1 = value
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
	println()

	// print solution for part 1
	println("*****************************")
	println("--- Day 25: Combo Breaker ---")
	println("*****************************")
	println("Solution for part1")
	println("   $solution1 is the encryption key handshake")
// end::part_1[]
//}	