from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("12/example2.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")

    pprint(result[:3])
    print()
    return result


def price(region: list[tuple[int, int]]) -> int:
    area = 0
    perimeter = 0
    return area * perimeter


def part1(data):
    """Solve and return the answer to part 1."""
    regions = []
    return sum([price(r) for r in regions])


def part2(data):
    """Solve and return the answer to part 2."""
    pass


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    solutions = solve(example_input)
    puzzle_input = get_data(day=12, year=2024)
    # solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
