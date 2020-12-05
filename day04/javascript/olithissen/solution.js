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
        .split("\r\n\r\n")
        .map(x => x.replace(/\r\n/g, " "))
        .map(x => x.split(" "))
        .map(x => {
            // this might actually be a reduce()
            let values = x.map(y => y.split(":"))
            let obj = {};
            values.forEach(value => obj[value[0]] = value[1]);
            return obj;
        });
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
    let props = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];
    return data
        .filter(passport => props.every(prop => passport.hasOwnProperty(prop)))
        .length;
}
//end::star1[]

//tag::star2[]
/**
 * Star 2
 */
function part2(data) {
    return data
        .filter(passport => Object.keys(check).every(key => check[key](passport[key])))
        .length;
}
//end::star2[]

//tag::checks[]
let check = {
    "byr": function (passportField) {
        let item = parseInt(passportField);
        return Number.isInteger(item) && item >= 1920 && item <= 2002;
    },

    "iyr": function (passportField) {
        let item = parseInt(passportField);
        return Number.isInteger(item) && item >= 2010 && item <= 2020;
    },

    "eyr": function (passportField) {
        let item = parseInt(passportField);
        return Number.isInteger(item) && item >= 2020 && item <= 2030;
    },

    "hgt": function (passportField) {
        const regex = /(\d+)(in|cm)/gm;
        let matches = regex.exec(passportField);

        if (matches == null) {
            return false;
        }

        let size = parseInt(matches[1]);

        if (matches[2] == "cm") {
            return size >= 150 && size <= 193;
        }

        if (matches[2] == "in") {
            return size >= 59 && size <= 76;
        }

        return false;
    },

    "hcl": function (passportField) {
        const regex = /^#[a-f0-9]{6}$/;
        return regex.test(passportField);
    },

    "ecl": function (passportField) {
        return ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"].indexOf(passportField) >= 0;
    },

    //tag::evilRegex[]
    "pid": function (passportField) {
        const regex = /^\d{9}$/;
        return regex.test(passportField);
    },
    //end::evilRegex[]

    "cid": function (passportField) {
        return true;
    }
}
//end::checks[]

const testdata = readAndTokenizeInput("./testdata.txt");
const valid = readAndTokenizeInput("./valid.txt");
const invalid = readAndTokenizeInput("./invalid.txt");
const data = readAndTokenizeInput("./input.txt");

runner(testdata, [{ funct: part1, exp: 2 }, { funct: part2, exp: 2 }], "Test data");
runner(valid, [{ funct: part1, exp: 4 }, { funct: part2, exp: 4 }], "Only valid");
runner(invalid, [{ funct: part1, exp: 4 }, { funct: part2, exp: 0 }], "Only invalid");
runner(data, [{ funct: part1, exp: 226 }, { funct: part2, exp: 160 }], "Real data");