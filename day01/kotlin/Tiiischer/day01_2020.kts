import java.io.File
import.kotlin.math.*

fun add_two_coins(): Int {
  var result: Int= 0
  file("Day01_2020Input.txt").forEachLine {
    var value1 = it.toInt()
    file("Day01_2020Input.txt").forEachLine {
      var value2 = it.toInt()
      if (value1 != value2) {
        if ((value1 + value2) == 2020 {
            result =value1 * value2
            }
        }
     }
  }
  return result
}

 var solution1: Int
 
            solution1 = add_two_coins()
            
            // print solution for part 1
	println("****************************")
	println("--- Day 1: Report Repair ---")
	println("****************************")
	println("Solution for part1")
	println("   $solution1 ")
	println()
