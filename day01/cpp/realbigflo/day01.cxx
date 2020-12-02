#include <fstream>
#include <iostream>
#include <string>
#include <vector>

constexpr int WANTED_SUM = 2020;

std::vector<int> get_numbers_from_file() {
  std::fstream in_file;
  std::string line;
  std::vector<int> numbers;
  in_file.open("input.txt", ::std::ios_base::in);
  while (getline(in_file, line)) {
    numbers.push_back(std::stoi(line));
  }

  return numbers;
}

int get_result_of_2(const std::vector<int> &numbers) {
  int outer = 0;
  for (auto iter_out = numbers.cbegin(); iter_out != numbers.cend();
       ++iter_out, ++outer) {
    auto iter_inner = numbers.cbegin() + outer;
    while (iter_inner != numbers.cend()) {
      if (*iter_out + *iter_inner == WANTED_SUM) {
        return *iter_out * *iter_inner;
      }
      ++iter_inner;
    }
  }
  return 0;
}

int get_result_of_3(const std::vector<int> &numbers) {
  for (int outer = 0; outer < numbers.size(); ++outer) {
    for (int inner = outer + 1; inner < numbers.size(); ++inner) {
      for (int sec_inner = inner + 1; sec_inner < numbers.size(); ++sec_inner) {
        if (numbers.at(outer) + numbers.at(inner) + numbers.at(sec_inner) ==
            WANTED_SUM) {
          return numbers.at(outer) * numbers.at(inner) * numbers.at(sec_inner);
        }
      }
    }
  }
  return 0;
}

int main() {
  const auto numbers = get_numbers_from_file();
  int result = get_result_of_2(numbers);
  std::cout << "Star1: the result is: " << result << "\n";
  result = get_result_of_3(numbers);
  std::cout << "Star1: the result is: " << result << "\n";
  return 0;
}