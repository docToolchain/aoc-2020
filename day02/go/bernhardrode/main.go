package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

// PasswordObject to be parsed
type PasswordObject struct {
	min      int
	max      int
	c        string
	password string
}

// GetInput of file as int
func GetInput(filename string) ([]PasswordObject, error) {
	file, err := os.Open(filename)

	if err != nil {
		log.Fatal(err)
	}

	sc := bufio.NewScanner(file)
	var result []PasswordObject

	for sc.Scan() {
		var min int
		var max int
		var c string
		var password string

		splits := strings.Split(sc.Text(), " ")
		minmax := strings.Split(splits[0], "-")

		min, _ = strconv.Atoi(minmax[0])
		max, _ = strconv.Atoi(minmax[1])
		c = strings.Replace(splits[1], ":", "", -1)
		password = splits[2]

		result = append(result, PasswordObject{min, max, c, password})
	}

	return result, sc.Err()
}

// ValidatePassword validates a password
func ValidatePassword(p PasswordObject) bool {
	counter := 0
	splits := strings.Split(p.password, "")

	for i := range splits {
		if splits[i] == p.c {
			counter = counter + 1
		}
	}
	return counter >= p.min && counter <= p.max
}

// ValidatePasswordToboggan validates a password
func ValidatePasswordToboggan(p PasswordObject) bool {
	splits := strings.Split(p.password, "")

	return (splits[p.min-1] == p.c && splits[p.max-1] != p.c) || (splits[p.min-1] != p.c && splits[p.max-1] == p.c)
}

// PartOne fn
func PartOne(input []PasswordObject) int {
	counter := 0
	for i := range input {
		if ValidatePassword(input[i]) {
			counter = counter + 1
		}
	}
	return counter
}

// PartTwo fn
func PartTwo(input []PasswordObject) int {
	counter := 0
	for i := range input {
		if ValidatePasswordToboggan(input[i]) {
			counter = counter + 1
		}
	}
	return counter
}

// main function
func main() {
	var filename = flag.String("f", "example", "Filename to get input from")
	flag.Parse()

	input, err := GetInput(*filename)
	if err != nil {
		return
	}

	var validPasswords int

	start := time.Now()
	validPasswords = PartOne(input)
	fmt.Println("PartOne", time.Since(start), validPasswords)

	start = time.Now()
	validPasswords = PartTwo(input)
	fmt.Println("PartTwo", time.Since(start), validPasswords)
}
