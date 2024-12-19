from pprint import pprint

import networkx as nx
from aocd import get_data
from dotenv import load_dotenv

with open("16/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> tuple[nx.DiGraph, complex]:
    """Parse input."""
    result = nx.DiGraph()
    grid = puzzle_input.split("\n")

    HEIGHT = len(grid)
    WIDTH = len(grid[0])
    START = 1 + ((HEIGHT - 2) * 1j)
    END = (WIDTH - 2) + 1j
    directions = [1j, 1, -1j, -1]  # N, E, S, W

    # Build nodes of the graph first
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == "#":
                continue  # This is a wall, so just skip

            pos = x + (y * 1j)  # Represent position as an imaginary number

            for dir in directions:
                n = (pos, dir)  # Nodes will be 2-tuple of (position, direction facing)
                result.add_node(n)

    # Build edges next
    for node in result.nodes:
        pos, dir = node
        step = (pos + dir, dir)
        if step in result.nodes:
            result.add_edge(node, step, weight=1)
        for rotation in -1j, 1j:
            result.add_edge(node, (pos, dir * rotation), weight=1000)

    # Set an edge from each possible end node (coming from any direction) to some imaginary 'final' node
    for dir in directions:
        result.add_edge((END, dir), "final", weight=0)

    pprint(grid[:3])
    print()
    return (result, START)


def part1(data: tuple[nx.DiGraph, complex]) -> int:
    """Solve and return the answer to part 1."""
    graph, start = data
    return nx.shortest_path_length(G=graph, source=(start, 1), target="final", weight="weight")


def part2(data: tuple[nx.DiGraph, complex]) -> int:
    """Solve and return the answer to part 2."""
    graph, start = data
    paths = nx.all_shortest_paths(G=graph, source=(start, 1), target="final", weight="weight")

    best_positions = set()
    for path in paths:
        for pos, dir in path[:-1]:
            best_positions.add(pos)

    return len(best_positions)


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=16, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
