import java.io.File

var text = ""

File("./day00_input.txt").forEachLine {
    text = it 
    println(text)
}
