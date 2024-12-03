import re

from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint

example_input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""


def parse(puzzle_input: str) -> str:
    """Parse input."""
    result = "do()" + puzzle_input + "don't()"

    pprint(result[:3])
    print()
    return result

def mul(s: str) -> int:
    """Helper function to take in a `mul` operation and actually calculate it"""
    left_num, right_num = s.split(",")
    
    left_num = int(left_num[4:])
    right_num = int(right_num[:-1])
    
    return left_num * right_num

def part1(data: str) -> int:
    """Solve and return the answer to part 1."""
    mul_pattern = r"mul\(\d+,\d+\)"
    
    mul_instructions = re.findall(mul_pattern, data)
    return sum([mul(i) for i in mul_instructions])


def part2(data: str) -> int:
    """Solve and return the answer to part 2."""
    do_dont_pattern = r"do\(\)(.*?)don't\(\)"
    valid_substrings_to_search = re.findall(do_dont_pattern, data, re.DOTALL)
    
    mul_pattern = r"mul\(\d+,\d+\)"

    result = 0
    for substring in valid_substrings_to_search:
        mul_instructions = re.findall(mul_pattern, substring)
        result += sum([mul(instruction) for instruction in mul_instructions])
        
    return result


def solve(puzzle_input: str) -> tuple:
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