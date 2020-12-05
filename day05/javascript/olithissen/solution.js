#!/usr/bin/env node

const fs = require("fs");
const assert = require("assert");
const { performance, PerformanceObserver } = require("perf_hooks");

const obs = new PerformanceObserver(list => {
    list.getEntries().forEach(item => console.log(item.name + ": " + item.duration));
    obs.disconnect();
});


//tag::readInput[]
/**
 * Reads the input file
 */
function readAndTokenizeInput(file) {
    return fs.readFileSync(file, "utf8")
        .split("\n")
}
//end::readInput[]

/**
 * Runners, reference tests and performance data
 */
function runner(data, functs, name = "Test") {
    console.log(name);
    functs.forEach(element => {
        var result = element.funct(data);
        console.log(" - " + element.funct.name + " result: " + result + ", expected: ", element.exp);
        if (element.hasOwnProperty('exp')) {
            assert(result == element.exp)
        }
    });
}

//tag::star1[]
/**
 * Star 1
 */
function part1(data) {
    let result = seats(data).map(x => x.id);

    return Math.max(...result);
}
//end::star1[]

// tag::parseSeats[]
function seats(data) {
    return data
        .map(x => x.replace(/(F|L)/g, "0").replace(/(B|R)/g, "1"))
        .map(x => {
            return {
                row: parseInt(x.substring(0, 7), 2),
                seat: parseInt(x.substring(7), 2),
                id: parseInt(x, 2),
            };
        });
}
//end::parseSeats[]

//tag::star2[]
/**
 * Star 2
 */
function part2(data) {
    let result = seats(data).map(x => x.id);

    let max = Math.max(...result);
    let min = Math.min(...result);

    for (let i = min; i < max; i++) {
        if (result.indexOf(i) == -1) {
            return i;
        }
    }
}
//end::star2[]


const testdata = readAndTokenizeInput("./testdata.txt");
const data = readAndTokenizeInput("./input.txt");

runner(testdata, [{ funct: part1, exp: 820 }, { funct: part2 }], "Test data");
runner(data, [{ funct: part1, exp: 901 }, { funct: part2, exp: 661 }], "Real data");
