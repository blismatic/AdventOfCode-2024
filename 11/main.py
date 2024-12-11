from functools import cache
from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("11/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> list[int]:
    """Parse input."""
    result = [int(stone) for stone in puzzle_input.split(" ")]

    pprint(result[:3])
    print()
    return result


@cache
def blink(stone: int, n: int) -> int:
    """Returns the number of stones that will appear after n number of blinks

    Args:
        stone (int): The number on a given stone
        n (int): How many times to blink

    Returns:
        int: The number of stones that will appear after n blinks
    """
    # Base case. If you don't blink at all, 1 stone will stay 1 stone.
    if n == 0:
        return 1

    # Rule 1
    if stone == 0:
        return blink(1, n - 1)

    # Rule 2
    stone_as_str = str(stone)
    if len(stone_as_str) % 2 == 0:
        left = int(stone_as_str[: len(stone_as_str) // 2])
        right = int(stone_as_str[len(stone_as_str) // 2 :])
        return blink(left, n - 1) + blink(right, n - 1)

    # Rule 3
    return blink(stone * 2024, n - 1)


def part1(data: list[str]) -> int:
    """Solve and return the answer to part 1."""
    d = data.copy()
    results = [blink(stone, 25) for stone in d]
    return sum(results)


def part2(data: list[str]) -> int:
    """Solve and return the answer to part 2."""
    d = data.copy()
    results = [blink(stone, 75) for stone in d]
    return sum(results)


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=11, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
