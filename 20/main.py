from pprint import pprint
from typing import TypeAlias

from aocd import get_data
from dotenv import load_dotenv

with open("20/example_input.txt", "r") as infile:
    example_input = infile.read()


def get_distances(start: complex, grid: dict[complex, str]) -> dict[complex, int]:
    queue = [start]
    curr_distance = 0
    result = {}

    while queue:
        curr_pos = queue.pop()
        result[curr_pos] = curr_distance

        # Find the correct next direction look.
        # Once you find it, stop looking at other directions.
        for dir in [1j, 1, -1j, -1]:  # N, E, S, W
            new_pos = curr_pos + dir
            if (new_pos not in result) and (new_pos in grid and grid[new_pos] in ".SE"):
                queue.append(new_pos)
                curr_distance += 1
                break

    return result


def parse(puzzle_input: str) -> tuple[dict[complex, int], complex]:
    """Parse input."""
    result = puzzle_input.split("\n")

    height = len(result)
    width = len(result[0])

    grid = {}  # (0,0) is top left
    for y in range(height):
        for x in range(width):
            curr_pos = x + (y * 1j)
            grid[curr_pos] = result[y][x]
            if result[y][x] == "S":
                START_POS = curr_pos

    distances = get_distances(START_POS, grid)
    return distances, START_POS


def part1(data: tuple[dict[complex, int], complex]) -> int:
    """Solve and return the answer to part 1."""
    distances, START_POS = data
    CHEAT_TIME = 2
    REQUIRED_TIME_SAVE = 100


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
    puzzle_input = get_data(day=20, year=2024)
    # solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
