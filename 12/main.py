from collections import deque
from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("12/example.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str):
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


def move(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    dirs = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}

    x, y = pos
    dx, dy = dirs[direction]

    return (x + dx, y + dy)


def part1(data: dict[tuple[int, int], str]) -> int:
    """Solve and return the answer to part 1."""
    prices = []

    grid = data.copy()
    already_visited = set()  # This will be a global variable to track which positions we have already processed at some point

    for pos in grid:
        if pos in already_visited:
            continue

        region_area = 0
        region_perimeter = 0
        q = deque()
        q.append(pos)

        # Keep exploring as long as the queue is not empty.
        while q:
            curr_pos = q.pop()
            if curr_pos in already_visited:
                continue
            else:
                already_visited.add(curr_pos)  # Add current position so that we won't ever analyze this position again
                region_area += 1

                neighbors = [move(curr_pos, direction) for direction in ["N", "E", "S", "W"]]
                for n in neighbors:
                    if n in grid and grid[n] == grid[curr_pos]:  # If the neighbor is a valid position *and* of the same plant type
                        q.append(
                            n
                        )  # Add this neighboring position to the queue, so that it will also be explored (since it must be part of the same region)
                    else:
                        region_perimeter += 1

        # After the queue is empty / exhausted, we know that the region's area/perimeter must be fully explored
        region_price = region_area * region_perimeter
        prices.append(region_price)

    result = sum(prices)
    return result


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
    puzzle_input = get_data(day=12, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))