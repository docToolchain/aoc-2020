#!/usr/bin/env node

const fs = require("fs");
const assert = require("assert");
const { performance, PerformanceObserver } = require("perf_hooks");

const obs = new PerformanceObserver(list => {
    list.getEntries().forEach(item => console.log(item.name + ": " + item.duration));
    obs.disconnect();
});


/**
 * Reads an input file
 */
function readAndTokenizeInput(file) {
    return fs.readFileSync(file, "utf8").split("\r\n").map(x => {
        const regex = /(\d+)-(\d+)\s(\S):\s(\S+)/gm;
        var m = regex.exec(x);
        return { "min": m[1], "max": m[2], "char": m[3], "passwd": m[4] };
    });
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
    return data.filter(item => {
        let occurence = Array.from(item.passwd).filter(c => c === item.char).length;
        return occurence >= item.min && occurence <= item.max;
    }).length;
}

/**
 * Part 2
 */
function part2(data) {
    return data.filter(item => {
        return validatePasswd(item);
    }).length;  
}

function validatePasswd(passwdData) {
    let pos1 = passwdData.passwd.charAt(passwdData.min - 1);
    let pos2 = passwdData.passwd.charAt(passwdData.max - 1);

    return (pos1 == passwdData.char || pos2 == passwdData.char) && pos1 != pos2;
}

const testdata = readAndTokenizeInput("./testdata.txt");
const data = readAndTokenizeInput("./input.txt");

runner(testdata, [{funct: part1, exp: 2}, {funct: part2, exp: 1}]);
runner(data, [{funct: part1, exp: 434}, {funct: part2, exp: 509}]);