#!/usr/bin/env groovy

//tag::readInput[]
myMap = new File("input.txt").text
                        .split("\n")
//end::readInput[]

//tag::star1[]
def readMap( x, y) {
    if (y>=myMap.size()) {
        return " "
    } else {
        return myMap[y][x%(myMap[0].size())]
    }
}
def countTrees(slope) {
    def trees = 0
    def x = 0
    def y = 0
    myMap.size().times {
        x = x+slope.x
        y = y+slope.y
        if (readMap(x,y)=="#") {
            trees++
        }
    }
    return trees
}
println countTrees([x:3,y:1])
//end::star1[]

//tag::star2[]
def solution = [
    [x:1,y:1],
    [x:3,y:1],
    [x:5,y:1],
    [x:7,y:1],
    [x:1,y:2]
].collect { slope -> 
    countTrees (slope)
}.inject(1) { result, item ->
    result * item
}
println solution
//end::star2[]
