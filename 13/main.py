import re
from pprint import pprint
from typing import TypeAlias

from aocd import get_data
from dotenv import load_dotenv

Machine: TypeAlias = tuple[int, int, int, int, int, int]

with open("13/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> list[Machine]:
    """Parse input."""
    numbers = [int(n) for n in re.findall(r"\d+", puzzle_input)]
    result = [tuple(numbers[i : i + 6]) for i in range(0, len(numbers), 6)]
    pprint(result[:3])
    print()
    return result


def get_cost(m: Machine, is_p2: bool = False) -> int:
    a_x, b_x, a_y, b_y, p_x, p_y = m
    if is_p2:
        p_x += 10_000_000_000_000
        p_y += 10_000_000_000_000

    # Cramer's rule: https://en.wikipedia.org/wiki/Cramer%27s_rule
    numerator = (p_x * b_y) - (a_y * p_y)
    denominator = (a_x * b_y) - (a_y * b_x)
    x = numerator / denominator

    numerator = (a_x * p_y) - (p_x * b_x)
    denominator = (a_x * b_y) - (a_y * b_x)
    y = numerator / denominator

    # Validate that x and y are both integers. You can't press a button 1.337 times!
    # x = number of A presses, y = number of B presses
    if (int(x) == x) and (int(y) == y):
        cost_of_prize = (int(x) * 3) + (int(y) * 1)
        return cost_of_prize
    else:
        return 0


def part1(data: list[Machine]) -> int:
    """Solve and return the answer to part 1."""
    costs = [get_cost(machine) for machine in data]
    result = sum(costs)
    return result


def part2(data: list[Machine]) -> int:
    """Solve and return the answer to part 2."""
    costs = [get_cost(machine, is_p2=True) for machine in data]
    result = sum(costs)
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
    puzzle_input = get_data(day=13, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
