from pprint import pprint

import networkx as nx
from aocd import get_data
from dotenv import load_dotenv

SIZE = 71
SRC = (0, 0)
TRGT = (SIZE - 1, SIZE - 1)

with open("18/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> list[tuple[int, int]]:
    """Parse input."""
    result = puzzle_input.split("\n")
    result = [(int(row.split(",")[0]), int(row.split(",")[1])) for row in result]

    pprint(result[:3])
    print()
    return result


def move(p1: tuple[int, int], dir: str) -> tuple[int, int]:
    directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

    x, y = p1
    dx, dy = directions[dir]

    return (x + dx, y + dy)


def part1(data: list[tuple[int, int]]) -> int:
    """Solve and return the answer to part 1."""
    grid = {}
    for x in range(SIZE):
        for y in range(SIZE):
            grid[(x, y)] = "."

    for pos in data[:1024]:
        grid[pos] = "#"

    G = nx.Graph()
    for pos, char in grid.items():
        if char == ".":
            neighbors = [move(pos, d) for d in ["N", "E", "S", "W"]]
            for n in neighbors:
                if n in grid and grid[n] == ".":
                    G.add_edge(pos, n)

    result = nx.shortest_path_length(G, source=SRC, target=TRGT)

    return result


def part2(data: list[tuple[int, int]]) -> str:
    """Solve and return the answer to part 2."""

    grid = {}
    for x in range(SIZE):
        for y in range(SIZE):
            grid[(x, y)] = "."

    # Create graph by adding edges
    G = nx.Graph()
    for pos in grid:
        neighbors = [move(pos, d) for d in ["N", "E", "S", "W"]]
        for n in neighbors:
            if n in grid:
                G.add_edge(pos, n)

    # Continually remove one node at a time and check that there is a valid path
    for pos in data:
        grid[pos] = "#"

        G.remove_node(pos)
        try:
            nx.shortest_path_length(G, source=SRC, target=TRGT)
        except nx.exception.NetworkXNoPath:
            x, y = pos
            return ",".join([str(x), str(y)])


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=18, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
