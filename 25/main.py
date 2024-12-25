from pprint import pprint
from typing import TypeAlias

import numpy as np
from aocd import get_data
from dotenv import load_dotenv

with open("25/example_input.txt", "r") as infile:
    example_input = infile.read()

Component: TypeAlias = list[int]


def parse(puzzle_input: str) -> tuple[list[Component], list[Component]]:
    """Parse input."""
    result = puzzle_input.split("\n\n")
    keys = []
    locks = []

    for elem in result:
        rows = elem.split("\n")
        cmp = np.array([list(row) for row in rows])
        cmp = np.rot90(cmp, -1)
        num_representation = [sum([True for e in pin if e == "#"]) - 1 for pin in cmp]
        if rows[0] == "#####":
            locks.append(num_representation)
        else:
            keys.append(num_representation)

    pprint(locks)
    print()
    return keys, locks


def part1(data: tuple[list[Component], list[Component]]) -> int:
    """Solve and return the answer to part 1."""
    keys, locks = data
    AVAILABLE_SPACE = 5

    pair_count = 0
    for lock in locks:
        for key in keys:
            fit = True
            for i in range(5):
                if key[i] + lock[i] > AVAILABLE_SPACE:
                    fit = False
                    break

            if fit:
                pair_count += 1

    return pair_count


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
    # solutions = solve(example_input)
    puzzle_input = get_data(day=25, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
