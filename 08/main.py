import string
from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

example_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


def parse(puzzle_input: str) -> dict[tuple[int, int], str]:
    """Parse input."""
    result = puzzle_input.split("\n")
    height = len(result)
    width = len(result[0])

    grid = {}
    for y in range(height):
        for x in range(width):
            grid[(x, height - y - 1)] = result[y][x]

    pprint(result[:3])
    print()
    return grid


def part1(data):
    """Solve and return the answer to part 1."""
    grid: dict[tuple[int, int], str] = data
    frequencies = string.ascii_letters + string.digits
    frequencies = [f for f in frequencies if f in grid.values()]
    unique_antinode_positions = set()

    for f in frequencies:
        locations = [
            pos for pos, char in grid.items() if char == f
        ]  # this will be a list of 2-tuples, like [(1, 3), (4, 2), (7, 7)]
        for i, loc in enumerate(locations):
            x, y = loc
            siblings = locations[:i] + locations[i + 1 :]

            for s in siblings:
                dx, dy = (x - s[0], y - s[1])
                antinode_pos = (x + dx, y + dy)
                print(antinode_pos)
                if antinode_pos in grid:
                    unique_antinode_positions.add(antinode_pos)

    return len(unique_antinode_positions)


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
    puzzle_input = get_data(day=8, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
