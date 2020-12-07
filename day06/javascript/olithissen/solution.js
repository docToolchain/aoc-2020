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
    const answers = fs.readFileSync(file, "utf8")
        .split("\r\n\r\n")
        .map(g => g.split("\r\n"));
    return answers;
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
    let items = data
        .map(answer => [...new Set(answer.join('').split('').sort())])
        .map(answer => answer.length)
        .reduce((acc, cur) => acc + cur);
    return items;
}
//end::star1[]


//tag::star2[]
/**
 * Star 2
 */
function part2(data) {
    let items = data
        .map(answer => {
            let sorted = answer.join('').split('').sort().join('');
            let letterGroups = sorted.match(/(\S)\1*/g);
            return letterGroups.filter(letterGroup => letterGroup.length == answer.length).length;
        })
        .reduce((acc, cur) => acc + cur);
    return items;
}
//end::star2[]


const testdata = readAndTokenizeInput("./testdata.txt");
const data = readAndTokenizeInput("./input.txt");

runner(testdata, [{ funct: part1, exp: 11 }, { funct: part2, exp: 6 }], "Test data");
runner(data, [{ funct: part1, exp: 6273 }, { funct: part2, exp: 3254 }], "Real data");
