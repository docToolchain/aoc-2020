#!/usr/bin/env groovy

//tag::readInput[]
def report = new File("input.txt").text
                        .split("\n")
                        .collect { 
                            it.trim() as Integer 
                        }
//end::readInput[]

//tag::star1[]
report.each { a ->
    report.each { b ->
        if (a+b==2020) {
            println a*b
        }
    }
}
//end::star1[]

//tag::star2[]
report.each { a ->
    report.each { b ->
        report.each { c ->
            if (a+b+c==2020) {
                println a*b*c
            }
        }
    }
}
//end::star2[]
