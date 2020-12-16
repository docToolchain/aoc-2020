import java.io.File

fun seats_occupied_2_rework_4(): Int {
    var grid = CharArray(0)
    var width: Int = -1
    File("day2011_puzzle_input.txt").forEachLine {
        // if this is the first line, set the width
        if (width == -1) {
            width = it.length
            grid = it.toCharArray()
        } else {
            var tmp = CharArray(grid.size + width)
            System.arraycopy(grid, 0, tmp, 0, grid.size)
            System.arraycopy(it.toCharArray(), 0, tmp, grid.size, width)
            grid = tmp
        }
    }
    var height: Int = grid.size / width

    var sum: Int
    var grid_new = CharArray(grid.size)
    var gameend: Boolean = false

    // directions
    var dlts = listOf(
            Pair(0, -1), // up
            Pair(1, -1), // up-right
            Pair(1, 0), // right
            Pair(1, 1), // down-right
            Pair(0, 1), // down
            Pair(-1, 1), // down-left
            Pair(-1, 0), // left
            Pair(-1, -1) // up-left
    )

    while (!gameend) {
        gameend = true

        var idx: Int = 0
        grid.forEach {
            var texture = it

            // sum over occupied seats
            sum = 0

            for (dlt in dlts) {
                var (dx, dy) = dlt
                // convert 1D index to x and y
                var x = idx % width + dx
                var y = idx / width + dy
                // since the list has no default, we need to check the bounds
                // to only do this once, the distinction between the cases is done inside the while loop
                while (x >= 0 && x < width && y >= 0 && y < height) {
                    if (grid[x + y * width] == '.') {
                        x += dx
                        y += dy
                    } else {
                        if (grid[x + y * width] == '#') {
                            sum++
                        }
                        break
                    }
                }
            }

            // more compact assignment of updated value
            grid_new[idx] = when {
                texture == 'L' && sum == 0 -> {
                    // free becomes occupied
                    gameend = false
                    '#'
                }
                texture == '#' && sum > 4 -> {
                    // occupied becomes free
                    gameend = false
                    'L'
                }
                else -> texture // no change
            }

            // increment counter
            idx++
        }

        grid = grid_new
        grid_new = CharArray(grid.size)
    } // gameend

    return grid.filter { it == '#' }.count()
}

fun seats_occupied_2_rework_3(): Int {
    var grid = mutableListOf<Char>()
    var width: Int = -1
    File("day2011_puzzle_input.txt").forEachLine {
        // if this is the first line, set the width
        if (width == -1) {
            width = it.length
        }
        it.forEach { grid.add(it) }
    }
    var height: Int = grid.size / width

    var sum: Int
    var grid_new = mutableListOf<Char>()
    var gameend: Boolean = false

    // directions
    var dlts = listOf(
            Pair(0, -1), // up
            Pair(1, -1), // up-right
            Pair(1, 0), // right
            Pair(1, 1), // down-right
            Pair(0, 1), // down
            Pair(-1, 1), // down-left
            Pair(-1, 0), // left
            Pair(-1, -1) // up-left
    )

    while (!gameend) {
        gameend = true

        var idx: Int = 0
        grid.forEach {
            var texture = it

            // sum over occupied seats
            sum = 0

            for (dlt in dlts) {
                var (dx, dy) = dlt
                // convert 1D index to x and y
                var x = idx % width + dx
                var y = idx / width + dy
                // since the list has no default, we need to check the bounds
                // to only do this once, the distinction between the cases is done inside the while loop
                while (x >= 0 && x < width && y >= 0 && y < height) {
                    if (grid[x + y * width] == '.') {
                        x += dx
                        y += dy
                    } else {
                        if (grid[x + y * width] == '#') {
                            sum++
                        }
                        break
                    }
                }
            }

            // more compact assignment of updated value
            grid_new.add(when {
                texture == 'L' && sum == 0 -> {
                    // free becomes occupied
                    gameend = false
                    '#'
                }
                texture == '#' && sum > 4 -> {
                    // occupied becomes free
                    gameend = false
                    'L'
                }
                else -> texture // no change
            })

            // increment counter
            idx++
        }

        grid = grid_new
        grid_new = mutableListOf()
    } // gameend

    return grid.filter { it == '#' }.count()
}

fun seats_occupied_2_rework_2(): Int {
    var Grid = mutableMapOf<Pair<Int, Int>, Char>()
    var x: Int = 0
    var y: Int = 0

    File("day2011_puzzle_input.txt").forEachLine {
        it.forEach {
            Grid.put(Pair(x, y), it)
            x++
        }
        y++
        x = 0
    }

    var sum: Int
    var Grid_new = mutableMapOf<Pair<Int, Int>, Char>()
    var gameend: Boolean = false

    // directions
    var dlts = listOf(
            Pair(0, -1), // up
            Pair(1, -1), // up-right
            Pair(1, 0), // right
            Pair(1, 1), // down-right
            Pair(0, 1), // down
            Pair(-1, 1), // down-left
            Pair(-1, 0), // left
            Pair(-1, -1) // up-left
    )

    while (!gameend) {
        gameend = true
        Grid.forEach {
            var texture = it.value
            var xpos = it.key.first
            var ypos = it.key.second

            // sum over occupied seats
            sum = 0

            // cond{i}_vis are not needed, since checking all false equals sum == 0

            for (dlt in dlts) {
                var k = 1
                var (dx, dy) = dlt
                while (Grid.getOrDefault(Pair(xpos + k * dx, ypos + k * dy), '0') == '.') {
                    k++
                }
                if (Grid.getOrDefault(Pair(xpos + k * dx, ypos + k * dy), '0') == '#') {
                    sum++
                }
            }

            if (texture == 'L') {
                if (sum == 0) {
                    Grid_new.put(it.key, '#')
                    gameend = false
                } else {
                    Grid_new.put(it.key, 'L')
                }
            } else if (texture == '#') {
                if (sum > 4) {
                    Grid_new.put(it.key, 'L')
                    gameend = false
                } else {
                    Grid_new.put(it.key, '#')
                }
            } else {
                Grid_new.put(it.key, '.')
            }
        }

        // copying grid can be expensive and not required
        Grid = Grid_new
        Grid_new = mutableMapOf()
    } // gameend

    // counting can be expressed simpler
    return Grid.filter { it.value == '#' }.count()
}

fun seats_occupied_2_rework_1(): Int {
    var Grid = mutableMapOf<Pair<Int, Int>, Char>()
    var x: Int = 0
    var y: Int = 0

    File("day2011_puzzle_input.txt").forEachLine {
        it.forEach {
            Grid.put(Pair(x, y), it)
            x++
        }
        y++
        x = 0
    }

    var sum: Int
    var Grid_new = mutableMapOf<Pair<Int, Int>, Char>()
    var gameend: Boolean = false
    var count: Int = 0

    while (!gameend) {
        gameend = true
        Grid.forEach {
            var texture = it.value
            var xpos = it.key.first
            var ypos = it.key.second
            var xoff = 1
            var yoff = 1

            var cond1_vis: Boolean = false
            var cond2_vis: Boolean = false
            var cond3_vis: Boolean = false
            var cond4_vis: Boolean = false
            var cond5_vis: Boolean = false
            var cond6_vis: Boolean = false
            var cond7_vis: Boolean = false
            var cond8_vis: Boolean = false

            sum = 0

            // direction up
            while (Grid.getOrDefault(Pair(xpos, ypos - yoff), '0') == '.') {
                yoff++
            }
            if (Grid.getOrDefault(Pair(xpos, ypos - yoff), '0') == '#') {
                cond1_vis = true
                sum++
            }
            yoff = 1
            // direction up-rigth
            while (Grid.getOrDefault(Pair(xpos + xoff, ypos - yoff), '0') == '.') {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault(Pair(xpos + xoff, ypos - yoff), '0') == '#') {
                cond2_vis = true
                sum++
            }
            yoff = 1
            xoff = 1
            // direction rigth
            while (Grid.getOrDefault(Pair(xpos + xoff, ypos), '0') == '.') {
                xoff++
            }
            if (Grid.getOrDefault(Pair(xpos + xoff, ypos), '0') == '#') {
                cond3_vis = true
                sum++
            }
            xoff = 1
            // direction rigth-down
            while (Grid.getOrDefault(Pair(xpos + xoff, ypos + yoff), '0') == '.') {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault(Pair(xpos + xoff, ypos + yoff), '0') == '#') {
                cond4_vis = true
                sum++
            }
            yoff = 1
            xoff = 1
            // direction down
            while (Grid.getOrDefault(Pair(xpos, ypos + yoff), '0') == '.') {
                yoff++
            }
            if (Grid.getOrDefault(Pair(xpos, ypos + yoff), '0') == '#') {
                cond5_vis = true
                sum++
            }
            yoff = 1
            // direction down-left
            while (Grid.getOrDefault(Pair(xpos - xoff, ypos + yoff), '0') == '.') {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault(Pair(xpos - xoff, ypos + yoff), '0') == '#') {
                cond6_vis = true
                sum++
            }
            yoff = 1
            xoff = 1
            // direction left
            while (Grid.getOrDefault(Pair(xpos - xoff, ypos), '0') == '.') {
                xoff++
            }
            if (Grid.getOrDefault(Pair(xpos - xoff, ypos), '0') == '#') {
                cond7_vis = true
                sum++
            }
            xoff = 1
            // direction up-left
            while (Grid.getOrDefault(Pair(xpos - xoff, ypos - yoff), '0') == '.') {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault(Pair(xpos - xoff, ypos - yoff), '0') == '#') {
                cond8_vis = true
                sum++
            }

            if (texture == 'L') {
                if (!cond1_vis && !cond2_vis && !cond3_vis && !cond4_vis && !cond5_vis && !cond6_vis && !cond7_vis && !cond8_vis) {
                    Grid_new.put(it.key, '#')
                    gameend = false
                } else {
                    Grid_new.put(it.key, 'L')
                }
            } else if (texture == '#') {
                if (sum > 4) {
                    Grid_new.put(it.key, 'L')
                    gameend = false
                } else {
                    Grid_new.put(it.key, '#')
                }

            } else {
                Grid_new.put(it.key, '.')
            }
        }
        Grid.clear()
        Grid.putAll(Grid_new)
        Grid_new.clear()
    } // gameend

    Grid.forEach {
        if (it.value == '#') {
            count++
        }
    }
    return count
}

// tag::create_seat_plan_2[]
fun seats_occupied_2_alt(): Int {
    var Grid = mutableMapOf<String, String>()
    var x: Int = 0
    var y: Int = 0

    File("day2011_puzzle_input.txt").forEachLine {
        it.forEach {
            Grid.put(x.toString() + "=" + y.toString(), it.toString())
            x++
        }
        y++
        x = 0
    }

    var sum: Int
    var Grid_new = mutableMapOf<String, String>()
    var gameend: Boolean = false
    var count: Int = 0

    while (!gameend) {
        gameend = true
        Grid.forEach {
            var texture = it.value
            var position = it.key.split("=")
            var xpos = position[0].toInt()
            var ypos = position[1].toInt()
            var xoff = 1
            var yoff = 1
            var cond1_vis: Boolean = false
            var cond2_vis: Boolean = false
            var cond3_vis: Boolean = false
            var cond4_vis: Boolean = false
            var cond5_vis: Boolean = false
            var cond6_vis: Boolean = false
            var cond7_vis: Boolean = false
            var cond8_vis: Boolean = false
            sum = 0

            // tag::determine_status_next_visible_seat[]
            // direction up
            while (Grid.getOrDefault((xpos).toString() + "=" + (ypos - yoff).toString(), "0").equals(".")) {
                yoff++
            }
            if (Grid.getOrDefault((xpos).toString() + "=" + (ypos - yoff).toString(), "0").equals("#")) {
                cond1_vis = true
                sum++
            }
            yoff = 1
            // direction up-rigth
            while (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals(".")) {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals("#")) {
                cond2_vis = true
                sum++
            }
            yoff = 1
            xoff = 1
            // direction rigth
            while (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos).toString(), "0").equals(".")) {
                xoff++
            }
            if (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos).toString(), "0").equals("#")) {
                cond3_vis = true
                sum++
            }
            xoff = 1
            // direction rigth-down
            while (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals(".")) {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault((xpos + xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals("#")) {
                cond4_vis = true
                sum++
            }
            yoff = 1
            xoff = 1
            // direction down
            while (Grid.getOrDefault((xpos).toString() + "=" + (ypos + yoff).toString(), "0").equals(".")) {
                yoff++
            }
            if (Grid.getOrDefault((xpos).toString() + "=" + (ypos + yoff).toString(), "0").equals("#")) {
                cond5_vis = true
                sum++
            }
            yoff = 1
            // direction down-left
            while (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals(".")) {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos + yoff).toString(), "0").equals("#")) {
                cond6_vis = true
                sum++
            }
            yoff = 1
            xoff = 1
            // direction left
            while (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos).toString(), "0").equals(".")) {
                xoff++
            }
            if (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos).toString(), "0").equals("#")) {
                cond7_vis = true
                sum++
            }
            xoff = 1
            // direction up-left
            while (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals(".")) {
                yoff++
                xoff++
            }
            if (Grid.getOrDefault((xpos - xoff).toString() + "=" + (ypos - yoff).toString(), "0").equals("#")) {
                cond8_vis = true
                sum++
            }
            // end::determine_status_next_visible_seat[]

            if (texture.equals("L")) {
                if (!cond1_vis && !cond2_vis && !cond3_vis && !cond4_vis && !cond5_vis && !cond6_vis && !cond7_vis && !cond8_vis) {
                    Grid_new.put(it.key, "#")
                    gameend = false
                } else {
                    Grid_new.put(it.key, "L")
                }
            } else if (texture.equals("#")) {
                if (sum > 4) {
                    Grid_new.put(it.key, "L")
                    gameend = false
                } else {
                    Grid_new.put(it.key, "#")
                }

            } else {
                Grid_new.put(it.key, ".")
            }
        }
        Grid.clear()
        Grid.putAll(Grid_new)
        Grid_new.clear()
    } // gameend

    Grid.forEach {
        if (it.value.equals("#")) {
            count++
        }
    }
    return count
}
// end::create_seat_plan_2[]

// tag::create_seat_plan[]
fun seats_occupied_alt(): Int {
    var Grid = mutableMapOf<String, String>()
    var x: Int = 0
    var y: Int = 0

    File("day2011_puzzle_input.txt").forEachLine {
        it.forEach {
            Grid.put(x.toString() + "=" + y.toString(), it.toString())
            x++
        }
        y++
        x = 0
    }

    var sum: Int
    var Grid_new = mutableMapOf<String, String>()
    var gameend: Boolean = false
    var count: Int = 0

    while (!gameend) {
        gameend = true
        Grid.forEach {
            var texture = it.value
            var position = it.key.split("=")
            var xpos = position[0].toInt()
            var ypos = position[1].toInt()

            var cond1: Boolean
            var cond2: Boolean
            var cond3: Boolean
            sum = 0

            if (texture.equals("L")) {
                cond1 =
                        !Grid.getOrDefault(
                                (xpos - 1).toString() + "=" + (ypos - 1).toString(),
                                "."
                        ).equals("#") && !Grid.getOrDefault((xpos).toString() + "=" + (ypos - 1).toString(), ".").equals(
                                "#"
                        ) && !Grid.getOrDefault((xpos + 1).toString() + "=" + (ypos - 1).toString(), ".").equals("#")
                cond2 =
                        !Grid.getOrDefault(
                                (xpos - 1).toString() + "=" + (ypos).toString(),
                                "."
                        ).equals("#") && !Grid.getOrDefault((xpos + 1).toString() + "=" + (ypos).toString(), ".").equals(
                                "#"
                        )
                cond3 =
                        !Grid.getOrDefault(
                                (xpos - 1).toString() + "=" + (ypos + 1).toString(),
                                "."
                        ).equals("#") && !Grid.getOrDefault((xpos).toString() + "=" + (ypos + 1).toString(), ".").equals(
                                "#"
                        ) && !Grid.getOrDefault((xpos + 1).toString() + "=" + (ypos + 1).toString(), ".").equals("#")
                if (cond1 && cond2 && cond3) {
                    Grid_new.put(it.key, "#")
                    gameend = false
                } else {
                    Grid_new.put(it.key, "L")
                }
            } else if (texture.equals("#")) {
                if (Grid.getOrDefault((xpos - 1).toString() + "=" + (ypos - 1).toString(), ".").equals("#")) {
                    sum++
                }
                if (Grid.getOrDefault((xpos).toString() + "=" + (ypos - 1).toString(), ".").equals("#")) {
                    sum++
                }
                if (Grid.getOrDefault((xpos + 1).toString() + "=" + (ypos - 1).toString(), ".").equals("#")) {
                    sum++
                }
                if (Grid.getOrDefault((xpos - 1).toString() + "=" + (ypos).toString(), ".").equals("#")) {
                    sum++
                }
                if (Grid.getOrDefault((xpos + 1).toString() + "=" + (ypos).toString(), ".").equals("#")) {
                    sum++
                }
                if (Grid.getOrDefault((xpos - 1).toString() + "=" + (ypos + 1).toString(), ".").equals("#")) {
                    sum++
                }
                if (Grid.getOrDefault((xpos).toString() + "=" + (ypos + 1).toString(), ".").equals("#")) {
                    sum++
                }
                if (Grid.getOrDefault((xpos + 1).toString() + "=" + (ypos + 1).toString(), ".").equals("#")) {
                    sum++
                }
                if (sum > 3) {
                    Grid_new.put(it.key, "L")
                    gameend = false
                } else {
                    Grid_new.put(it.key, "#")
                }
            } else {
                Grid_new.put(it.key, ".")
            }
        }
        Grid.clear()
        Grid.putAll(Grid_new)
        Grid_new.clear()
    }

    Grid.forEach {
        if (it.value.equals("#")) {
            count++
        }
    }
    return count
}
// end::create_seat_plan[]

//fun main(args: Array<String>) {

// tag::part_1[]
var solution1 = seats_occupied_alt()
// end::part_1[]

// tag::part_2[]
var t2 = System.currentTimeMillis()
var solution2 = seats_occupied_2_alt()
t2 = System.currentTimeMillis() - t2
println("part 2 solved in $t2 ms -> XXXX")
// end::part_2[]

var t2_r1 = System.currentTimeMillis()
var solution2_r1 = seats_occupied_2_rework_1()
t2_r1 = System.currentTimeMillis() - t2_r1
println("part 2 rework 1 solved in $t2_r1 ms -> XXXX")

var t2_r2 = System.currentTimeMillis()
var solution2_r2 = seats_occupied_2_rework_2()
t2_r2 = System.currentTimeMillis() - t2_r2
println("part 2 rework 2 solved in $t2_r2 ms -> XXXX")

var t2_r3 = System.currentTimeMillis()
var solution2_r3 = seats_occupied_2_rework_3()
t2_r3 = System.currentTimeMillis() - t2_r3
println("part 2 rework 3 solved in $t2_r3 ms -> XXXX")

var t2_r4 = System.currentTimeMillis()
var solution2_r4 = seats_occupied_2_rework_4()
t2_r4 = System.currentTimeMillis() - t2_r4
println("part 2 rework 4 solved in $t2_r4 ms -> XXXX")

// tag::output[]
// print solution for part 1
println("****************************")
println("--- Day 11: Seating System ---")
println("****************************")
println("Solution for part1")
println("   XXXX seats end up occupied")
println()
// print solution for part 2
println("****************************")
println("Solution for part2")
println("   XXXX any seats end up occupied")
println()
// end::output[]
//}