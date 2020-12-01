import java.io.File

var breakFlag = false
var theAnswer = 0
var array_index = 0
var array_of_numbers = Array<Int>(200){0}

File("./day01_input.txt").forEachLine {
    array_of_numbers[array_index] = it.toInt()
    array_index++
}

for (xAxis in array_of_numbers){
    for (yAxis in array_of_numbers)
        if (xAxis+yAxis == 2020){
            print("Treffer")
            print(xAxis)
            print(yAxis)
            println("")
            breakFlag = true
            theAnswer = xAxis*yAxis
            break            
        }
    if (breakFlag == true)
        break
}

println(theAnswer)
