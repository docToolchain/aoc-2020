import java.io.File
import kotlin.math.*
	
	var text: String = ""

	File("day2000_puzzle_input.txt").forEachLine {
		 text = it
	}

	println("RJPlog like's $text")