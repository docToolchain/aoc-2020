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
function readInput(file) {
    return fs.readFileSync(file, "utf8").split("\r\n");
}
//end::readInput[]

/**
 * Runners, reference tests and performance data
 */
function runner(data, functs) {
    functs.forEach(element => {
        var result = element.funct(data);
        console.log("Result: " + result);
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
    return walk(data, 3, 1);
}
//end::star1[]

//tag::walk[]
function walk(data, x, y) {
    let width = data[0].length;
    let column = 0;
    let row = 0;
    let hits = 0;

    while (row + 1 < data.length) {
        column = (column + x) % width;
        row = row + y;
        if (data[row].charAt(column) == "#") {
            hits++;
        }
    }

    return hits;    
}
//end::walk[]

//tag::star2[]
/**
 * Star 2
 */
function part2(data) {
    let product = 1;
    product *= walk(data, 1, 1);
    product *= walk(data, 3, 1);
    product *= walk(data, 5, 1);
    product *= walk(data, 7, 1);
    product *= walk(data, 1, 2);
    return product;
}
//end::star2[]

const testdata = readInput("./testdata.txt");
const data = readInput("./input.txt");

runner(testdata, [{funct: part1, exp: 7}, {funct: part2, exp: 336}]);
runner(data, [{funct: part1, exp: 145}, {funct: part2}]);