import java.io.File

// tag::allergen_2[]
fun allergen_2(): String {

	// tag::read_puzzle[]	
	var food_ingredients = mutableMapOf<Int, List<String>>()
	var food_allergens = mutableMapOf<Int, List<String>>()
	var allergen_list = mutableMapOf<String, String>()
	var food: Int = 0

	File("day2021_puzzle_input.txt").forEachLine {
		var instruction = it.replace(",", "").replace(")", "").split(" (contains ")
		food_ingredients.put(food, instruction[0].split(" "))
		food_allergens.put(food, instruction[1].split(" "))
		instruction[1].split(" ").forEach {
			allergen_list.put(it, "-")
		}
		food++
	}
	// end::read_puzzle[]

	// tag::search[]
	var i: Int
	var temp_list1 = mutableListOf<String>()
	var temp_list2 = mutableListOf<String>()
	var new_list: String = ""

	for (m in 0..5) {
		allergen_list.forEach {
			if (it.value.equals("-")) {
				var allergen = it.key
				i = 0
				while (!food_allergens.getValue(i).contains(allergen)) {
					i++
				}
				temp_list1.clear()
				temp_list1.addAll(food_ingredients.getValue(i))
				for (j in i + 1..food - 1) {
					temp_list2.clear()
					temp_list2.addAll(food_ingredients.getValue(j))
					if (food_allergens.getValue(j).contains(allergen)) {
						temp_list1.retainAll(temp_list2)
					}
				}
				if (temp_list1.size == 1) {
					allergen_list.put(allergen, temp_list1[0])
					food_ingredients.forEach {
						for (k in 0..it.value.size - 1) {
							if (it.value[k] != temp_list1[0]) {
								new_list = new_list + it.value[k] + " "
							}
						}
						food_ingredients.put(it.key, new_list.dropLast(1).split(" "))
						new_list = ""
					}
				}
			} // end if
		}
	}
	// end::search[]	

	// tag::order_result[]
	var result: String = ""
	val sorted = allergen_list.toSortedMap()
	sorted.forEach {
		result = result + it.value + ","
    }
    result = result.dropLast(1)
	// end::order_result[]

	return result
}
// end::allergen_2[]

// tag::allergen[]
fun allergen(): Int {

	// tag::read_puzzle[]	
	var food_ingredients = mutableMapOf<Int, List<String>>()
	var food_allergens = mutableMapOf<Int, List<String>>()
	var allergen_list = mutableMapOf<String, String>()
	var food: Int = 0

	File("day2021_puzzle_input.txt").forEachLine {
		var instruction = it.replace(",", "").replace(")", "").split(" (contains ")
		food_ingredients.put(food, instruction[0].split(" "))
		food_allergens.put(food, instruction[1].split(" "))
		instruction[1].split(" ").forEach {
			allergen_list.put(it, "-")
		}
		food++
	}
	// end::read_puzzle[]

	// tag::search[]
	var i: Int
	var temp_list1 = mutableListOf<String>()
	var temp_list2 = mutableListOf<String>()
	var new_list: String = ""

	for (m in 0..5) {   // better to replace with while loop and a proper exitcondition
		allergen_list.forEach {
			if (it.value.equals("-")) {
				var allergen = it.key
				i = 0
				while (!food_allergens.getValue(i).contains(allergen)) {
					i++
				}
				temp_list1.clear()
				temp_list1.addAll(food_ingredients.getValue(i))
				for (j in i + 1..food - 1) {
					temp_list2.clear()
					temp_list2.addAll(food_ingredients.getValue(j))
					if (food_allergens.getValue(j).contains(allergen)) {
						temp_list1.retainAll(temp_list2)
					}
				}
				if (temp_list1.size == 1) {
					allergen_list.put(allergen, temp_list1[0])
					food_ingredients.forEach {
						for (k in 0..it.value.size - 1) {
							if (it.value[k] != temp_list1[0]) {
								new_list = new_list + it.value[k] + " "
							}
						}
						food_ingredients.put(it.key, new_list.dropLast(1).split(" "))
						new_list = ""
					}
				}
			}
		}
	}
	// end::search[]	

	// tag::count_result[]
	var result: Int = 0
	food_ingredients.forEach {
		result = result + it.value.size
	}
	// end::count_result[]

	return result
}
// end::allergen[]

//fun main(args: Array<String>) {

// tag::part_1[]
	var t1 = System.currentTimeMillis()
	var solution1 = allergen()
	t1 = System.currentTimeMillis() - t1
	println()
	println("part 1 solved in $t1 ms -> $solution1")
// end::part_1[]

// tag::part_2[]
	var t2 = System.currentTimeMillis()
	var solution2 = allergen_2()
	t2 = System.currentTimeMillis() - t2
	println()
	println("part 2 solved in $t2 ms -> $solution2")
// end::part_2[]

// tag::output[]
// print solution for part 1
	println("***********************************")
	println("--- Day 21: Allergen Assessment ---")
	println("***********************************")
	println("Solution for part1")
	println("   $solution1 times do any of those ingredients appear")
	println()
// print solution for part 2
	println("****************************")
	println("Solution for part2")
	println("   $solution2 is your canonical dangerous ingredient list")
	println()
// end::output[]
//}	