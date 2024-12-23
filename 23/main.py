from pprint import pprint

import networkx as nx
from aocd import get_data
from dotenv import load_dotenv

with open("23/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> nx.Graph:
    """Parse input."""
    result = puzzle_input.split("\n")
    G = nx.Graph()
    for connection in result:
        c1, c2 = connection.split("-")
        G.add_edge(c1, c2)

    pprint(result[:3])
    print()
    return G


def part1(data: nx.Graph) -> int:
    """Solve and return the answer to part 1."""
    triplets = [clique for clique in nx.enumerate_all_cliques(data) if len(clique) == 3]
    t_computer_triplets = [clique for clique in triplets if any(node.startswith("t") for node in clique)]
    return len(t_computer_triplets)


def part2(data: nx.Graph) -> str:
    """Solve and return the answer to part 2."""
    max_clique = max(nx.find_cliques(data), key=len)
    return ",".join(sorted(max_clique))


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=23, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
