#!/usr/bin/env groovy

//tag::readInput[]
passports = []
passport = [:]

new File("input.txt").eachLine { line ->
    if (line.trim()=="") {
        passports << passport
        passport = [:]
    } else {
        line.split(" ").each { entry ->
            entry = entry.split(":")
            passport[entry[0]]=entry[1]
        }
    }
}
passports << passport
//end::readInput[]

//tag::star1[]
Boolean hasNeededFields(passport) {
    entries = "byr iyr eyr hgt hcl ecl pid".split(" ")
    isValid = true
    entries.each { entry -> 
        if (passport[entry]==null) {
            isValid = false
        }
    }
    return isValid
}
println passports.findAll{passport-> hasNeededFields(passport)}.size()
//end::star1[]

//tag::star2[]
Boolean fieldsAreValid(passport) {
    def isValid = true
    if (!hasNeededFields(passport)) {
        isValid = false
    } else {
        // byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if (passport.byr==~ /[0-9]{4}/) {
            def byr = passport.byr as Integer
            if (byr<1920 || byr>2002) {
                isValid = false
            }
        } else {
            isValid = false
        }
        // iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if (passport.iyr==~ /[0-9]{4}/) {
            def iyr = passport.iyr as Integer
            if (iyr<2010 || iyr>2020) {
                isValid = false
            }
        } else {
            isValid = false
        }
        // eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if (passport.eyr==~ /[0-9]{4}/) {
            def eyr = passport.eyr as Integer
            if (eyr<2020 || eyr>2030) {
                isValid = false
            }
        } else {
            isValid = false
        }
        // hgt (Height) - a number followed by either cm or in:
            // If cm, the number must be at least 150 and at most 193.
            // If in, the number must be at least 59 and at most 76.
        if (passport.hgt ==~ /[0-9]+(cm|in)/) {
            hgt = passport.hgt
            if (hgt.contains("in")) {
                hgt = (hgt-"in") as Integer
                if (hgt<59 || hgt>76) {
                    isValid = false
                }
            } else {
                hgt = (hgt-"cm") as Integer
                if (hgt<150 || hgt>193) {
                    isValid = false
                }
            }
        } else {
            isValid = false
        }
        // hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        if (passport.hcl ==~ /#[0-9a-f]{6}/) {
        } else {
            isValid = false
        }
        // ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        if (passport.ecl ==~ /(amb|blu|brn|gry|grn|hzl|oth)/) {
        } else {
            isValid = false
        }
        // pid (Passport ID) - a nine-digit number, including leading zeroes.
        if (passport.pid ==~ /[0-9]{9}/) {
        } else {
            isValid = false
        }
    }
    return isValid
}
println passports.findAll{passport-> fieldsAreValid(passport)}.size()
//end::star2[]
