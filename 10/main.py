from collections import deque
from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("10/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> dict[tuple[int, int], int]:
    """Parse input."""
    result = puzzle_input.split("\n")

    height = len(result)
    width = len(result[0])

    grid = {}
    for y in range(height):
        for x in range(width):
            grid[(x, height - y - 1)] = int(result[y][x])

    pprint(result[:3])
    print()
    return grid


def move(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    ds = {"North": (0, 1), "East": (1, 0), "South": (0, -1), "West": (-1, 0)}

    x, y = pos
    dx, dy = ds[direction]

    return (x + dx, y + dy)


def get_score(grid: dict[tuple[int, int], int], trailhead: tuple[int, int]) -> int:
    dirs = ["North", "East", "South", "West"]
    score = 0
    q = deque(
        {
            trailhead,
        }
    )
    encountered_positions = set()

    while q:
        position = q.popleft()
        if position in encountered_positions:
            continue
        encountered_positions.add(position)
        elevation = grid[position]
        if elevation == 9:
            score += 1
            continue
        neighbor_positions = [move(position, d) for d in dirs]
        valid_neighbor_positions = [n for n in neighbor_positions if n in grid and grid[n] == elevation + 1]
        q.extend(valid_neighbor_positions)
    return score


def get_rating(grid: dict[tuple[int, int], int], trailhead: tuple[int, int]) -> int:
    dirs = ["North", "East", "South", "West"]
    score = 0
    q = deque(
        {
            trailhead,
        }
    )

    while q:
        position = q.popleft()
        elevation = grid[position]
        if elevation == 9:
            score += 1
            continue
        neighbor_positions = [move(position, d) for d in dirs]
        valid_neighbor_positions = [n for n in neighbor_positions if n in grid and grid[n] == elevation + 1]
        q.extend(valid_neighbor_positions)
    return score


def part1(data: dict[tuple[int, int], int]):
    """Solve and return the answer to part 1."""
    trailheads = [pos for pos, height in data.items() if height == 0]

    trail_scores = [get_score(data, th) for th in trailheads]
    return sum(trail_scores)


def part2(data: dict[tuple[int, int], int]):
    """Solve and return the answer to part 2."""
    trailheads = [pos for pos, height in data.items() if height == 0]

    trail_ratings = [get_rating(data, th) for th in trailheads]
    return sum(trail_ratings)


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=10, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
