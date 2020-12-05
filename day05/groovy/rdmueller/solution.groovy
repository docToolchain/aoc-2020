#!/usr/bin/env groovy

//tag::decodePass[]
def decodePass(pass) {
    def id = 0
    pass.each { 
        id = id << 1
        if (it in ["B", "R"]) {
            id+=1
        }
    }
    def row = id/8 as Integer
    def col = id%8
    return [row, col, id]
}

assert decodePass("BFFFBBFRRR") == [70,7,567]
//end::decodePass[]

//tag::star1[]
boardingpasses = new File("input.txt").text
                    .split("\n")
                    .collect{ pass ->
                        decodePass(pass)
                    }
def highestId = 0
boardingpasses.each { pass ->
    if (pass[2]>highestId) {
        highestId = pass[2]
    }
}
println highestId
//end::star1[]

//tag::star2[]
//find all IDs
def ids=[:]
boardingpasses.each { pass ->
    ids[pass[2]]=pass
}

//print all missing IDs, skip first ones
def skip=true
highestId.times { id ->
    if (ids[id]==null) {
        if (skip==false) {
            println id
        }
    } else {
        skip=false
    }
}
//end::star2[]