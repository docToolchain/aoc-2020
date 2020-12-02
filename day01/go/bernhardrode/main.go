package main

import (
	"bufio"
	"errors"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"
)

// GetInput of file as int
func GetInput(filename string) ([]int, error) {
	file, err := os.Open(filename)

	if err != nil {
		log.Fatal(err)
	}

	sc := bufio.NewScanner(file)
	sc.Split(bufio.ScanWords)
	var result []int

	for sc.Scan() {
		x, err := strconv.Atoi(sc.Text())
		if err != nil {
			return result, err
		}
		result = append(result, x)
	}

	return result, sc.Err()
}

// FindTwo numbers
func FindTwo(numbers []int, target int) (int, int, error) {
	result := make(map[int]int)

	for _, v := range numbers {
		result[target-v] = v
		if value, ok := result[v]; ok {
			return value, v, nil
		}
	}
	return 0, 0, errors.New("not_found")
}

// FindThree numbers
func FindThree(input []int, target int) (int, int, int, error) {
	for i, _ := range input[:len(input)-2] {
		start, end := i+1, len(input)-1
		fmt.Println("-", i, start, end)

		for start < end {
			sum := input[i] + input[start] + input[end]

			if sum > target {
				end--
			} else if sum < target {
				start++
			} else {
				return input[i], input[start], input[end], nil
			}
		}
	}
	return 0, 0, 0, errors.New("not_found")
}

// main function for aoc day01
func main() {
	var filename = flag.String("f", "example", "Filename to get input from")
	var year = flag.Int("y", 2020, "Year for expense reports")

	flag.Parse()

	input, err := GetInput(*filename)
	if err != nil {
		return
	}

	var n1 int
	var n2 int
	var n3 int

	start := time.Now()
	n1, n2, _ = FindTwo(input, *year)
	fmt.Println("FindTwo", time.Since(start), n1*n2)

	start = time.Now()
	n1, n2, n3, _ = FindThree(input, *year)
	fmt.Println("FindThree", time.Since(start), n1*n2*n3)
}
