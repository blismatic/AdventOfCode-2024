from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint

example_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")
    rows = [r.split(":") for r in result]
    result = [[int(row[0]), [int(n) for n in row[1].strip().split()]] for row in rows]

    pprint(result[:3])
    print()
    return result

def is_valid(t: int, nums: list[int], is_p2: bool = False) -> bool:
    if len(nums) == 1: # Base case
        return nums[0] == t
    else:
        add_path = [nums[0] + nums[1]] + nums[2:]
        multiply_path = [nums[0] * nums[1]] + nums[2:]
        concat_path = [int(str(nums[0]) + str(nums[1]))] + nums[2:]
        if is_valid(t, add_path, is_p2):
            return True
        elif is_valid(t, multiply_path, is_p2):
            return True
        elif is_p2 and is_valid(t, concat_path, is_p2):
            return True
        else:
            return False

def part1(data):
    """Solve and return the answer to part 1."""
    valid_targets = [eqs[0] for eqs in data if is_valid(eqs[0], eqs[1])]
    return sum(valid_targets)


def part2(data):
    """Solve and return the answer to part 2."""
    valid_targets = [eqs[0] for eqs in data if is_valid(eqs[0], eqs[1], is_p2=True)]
    return sum(valid_targets)


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=7, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))