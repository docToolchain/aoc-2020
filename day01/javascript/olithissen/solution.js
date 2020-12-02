#!/usr/bin/env node

const fs = require("fs");
const assert = require("assert");
const { performance, PerformanceObserver } = require("perf_hooks");

const obs = new PerformanceObserver(list => {
  list.getEntries().forEach(item => console.log(item.name + ": " + item.duration));
  obs.disconnect();
});

/**
 * Reads an input file as an array by splitting it char by char
 */
function readLinesAsNumericArray(file) {
  return fs.readFileSync(file, "utf8").split("\r\n").map(x => parseInt(x));
}

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

/**
 * Part 1
 */
function part1(data) {
    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data.length; j++) {
            if (data[i] + data[j] == 2020) {
                return data[i] * data[j];
            }
        }
    }
}

/**
 * Part 2
 */
function part2(data) {
    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data.length; j++) {
            for (var k = 0; k < data.length; k++) {
                if (data[i] + data[j] + data[k] == 2020) {
                    return data[i] * data[j] * data[k];
                }
            }
        }
    }
}

const testdata = readLinesAsNumericArray("./testdata.txt");
const data = readLinesAsNumericArray("./input.txt");

runner(testdata, [{funct: part1, exp: 514579}, {funct: part2, exp: 241861950}]);
runner(data, [{funct: part1, exp: 211899}, {funct: part2, exp: 275765682}]);