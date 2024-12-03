import re

from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint

example_input = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")

    pprint(result[:3])
    print()
    return result


def part1(data):
    """Solve and return the answer to part 1."""
    pattern = r"mul\(\d+,\d+\)"
    matches = re.findall(pattern, data[0])
    result = 0
    for line in data:
        matches = re.findall(pattern, line)
        for match in matches:
            l, r = match.split(",")
            l = l[4:]
            r = r[:-1]
            result += (int(l) * int(r))
    return result


def part2(data):
    """Solve and return the answer to part 2."""
    long_string = "do()" + "".join(data)
    pattern = r"mul\(\d+,\d+\)"
    pattern2 = r"do\(\)(.*?)don't\(\)"
    
    valid_substrings_to_search = re.findall(pattern2, long_string, re.DOTALL)
    # print(len(valid_substrings_to_search))
    result = 0

    for substring in valid_substrings_to_search:
        matches = re.findall(pattern, substring)
        for match in matches:
            l, r = match.split(",")
            l = l[4:]
            r = r[:-1]
            result += (int(l) * int(r))
    return result


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=3, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))