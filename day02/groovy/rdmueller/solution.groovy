#!/usr/bin/env groovy

//tag::readInput[]
def inputs = new File("input.txt").text
                        .split("\n")
                        .collect { 
                            def (rule,letter,pw) = it.split(" ")
                            rule = rule.split("-").collect{ it as Integer}
                            letter = letter-":"
                            [rule,letter,pw] 
                        }
//end::readInput[]

//tag::star1[]
Boolean isValid(rule, letter, pw) {
    def count = 0
    pw.each { pwLetter ->
        if (pwLetter==letter) {
            count++
        }
    }
    if (count>=rule[0] && count<=rule[1]) {
        return true
    } else {
        return false
    }
}
assert (isValid(*[[1,3], "a", "abcde"])==true)
assert (isValid(*[[1,3], "b", "cdefg"])==false)
def count = 0
inputs.each { input ->
    if (isValid(*input)) {
        count++
    }
}
println count
//end::star1[]

//tag::star2[]
Boolean isValid2(rule, letter, pw) {
    if (   (pw[rule[0]-1] == letter && pw[rule[1]-1] != letter)
        || (pw[rule[1]-1] == letter && pw[rule[0]-1] != letter) ) {
        return true
    } else {
        return false
    }
}
assert (isValid2(*[[1,3], "a", "abcde"])==true)
assert (isValid2(*[[1,3], "b", "cdefg"])==false)
def count2 = 0
inputs.each { input ->
    if (isValid2(*input)) {
        count2++
    }
}
println count2
//end::star2[]
