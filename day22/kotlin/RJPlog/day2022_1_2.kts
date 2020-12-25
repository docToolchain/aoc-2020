import java.io.File

// tag::crab_combat_2[]
fun crab_combat_2(stacks: Pair<MutableList<Int>, MutableList<Int>>, n: Int): Pair<Int, Int> {
	var result: Int
	var deck_1 = stacks.first
	var deck_2 = stacks.second
	var gameend: Boolean = false

	// setup list for infinite rule
	var played_decks = mutableListOf(Pair(deck_1.toMutableList(), deck_2.toMutableList()))

	while (!gameend) {
		var card_1 = deck_1[0]
		var card_2 = deck_2[0]
		deck_1.removeAt(0)
		deck_2.removeAt(0)

		// evaluate result, jump into recursive game or play accoring to the old rules
		if (deck_1.size >= card_1 && deck_2.size >= card_2) {
			// rule for starting a Recursive Combat
			var winner = crab_combat_2(
				Pair(deck_1.take(card_1).toMutableList(), deck_2.take(card_2).toMutableList()),
				n + 1
			).first
			// look how is the winner and create new deck!
			if (winner == 1) {
				deck_1.add(card_1)
				deck_1.add(card_2)
			} else if (winner == 2) {
				deck_2.add(card_2)
				deck_2.add(card_1)
			} else if (winner == 3) {
				deck_1.add(card_1)
				deck_1.add(card_2)
			}
		} else {
			// old_rule
			if (card_1 > card_2) {
				deck_1.add(card_1)
				deck_1.add(card_2)
			} else if (card_2 > card_1) {
				deck_2.add(card_2)
				deck_2.add(card_1)
			}
		}

		// check infinite rule
		if (played_decks.contains((Pair(deck_1.toMutableList(), deck_2.toMutableList())))) {
			return Pair(3, n - 1)
		} else {
			played_decks.add(Pair(deck_1.toMutableList(), deck_2.toMutableList()))
		}

		// check if game is finished
		if (deck_1.isEmpty()) {
			result = 0
			for (i in 0..deck_2.size - 1) {
				result = result + deck_2[i] * (deck_2.size - i)
			}
			return Pair(2, result)
		} else if (deck_2.isEmpty()) {
			result = 0
			for (i in 0..deck_1.size - 1) {
				result = result + deck_1[i] * (deck_1.size - i)
			}
			return Pair(1, result)
		}
	}
	return Pair(1, n - 1)
}
// end::crab_combat_2[]

// tag::crab_combat[]
fun crab_combat(stacks: Pair<MutableList<Int>, MutableList<Int>>): Int {
	var result: Int = 0
	var deck_1 = stacks.first
	var deck_2 = stacks.second
	var gameend: Boolean = false

	while (!gameend) {
		var card_1 = deck_1[0]
		var card_2 = deck_2[0]
		if (card_1 > card_2) {
			deck_1.add(card_1)
			deck_1.add(card_2)
		} else if (card_2 > card_1) {
			deck_2.add(card_2)
			deck_2.add(card_1)
		}
		deck_1.removeAt(0)
		deck_2.removeAt(0)
		if (deck_1.isEmpty()) {
			gameend = true
			for (i in 0..deck_2.size - 1) {
				result = result + deck_2[i] * (deck_2.size - i)
			}
		} else if (deck_2.isEmpty()) {
			gameend = true
			for (i in 0..deck_1.size - 1) {
				result = result + deck_1[i] * (deck_1.size - i)
			}
		}
	}
	return result
}
// end::crab_combat[]

// tag::read_puzzle[]
fun space_cards(): Pair<MutableList<Int>, MutableList<Int>> {
	var deck_1 = mutableListOf<Int>()
	var deck_2 = mutableListOf<Int>()
	var segment: Int = 0

	File("day2022_puzzle_input.txt").forEachLine {
		when (segment) {
			0 -> if (it.contains("Player 1")) {
				segment++
			}
			1 -> {
				if (it == "") {
					segment++
				} else {
					deck_1.add(it.toInt())
				}
			}
			2 -> {
				if (!it.contains("Player 2")) {
					deck_2.add(it.toInt())
				}
			}
		}
	}
	return Pair(deck_1, deck_2)
}
// end::read_puzzle[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = crab_combat(space_cards())
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = crab_combat_2(space_cards(), 1).second
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
	println()
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("***************************")
	println("--- Day 22: Crab Combat ---")
	println("***************************")
	println("Solution for part1")
	println("   $solution1 is the winning player's score.")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is the winning player's score.")
	println()
// end::output[]
//}	