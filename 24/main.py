from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("24/example_input2.txt", "r") as infile:
    example_input = infile.read()

operations = {"AND": (lambda a, b: int(a and b)), "OR": (lambda a, b: int(a or b)), "XOR": (lambda a, b: int(a != b))}


def parse(puzzle_input: str) -> tuple[dict[str, int], list[str]]:
    """Parse input."""
    initial_wire_values, connections = puzzle_input.split("\n\n")

    initial_wire_values = [wv for wv in initial_wire_values.split("\n")]
    initial_wire_values = [[w, int(v)] for item in initial_wire_values for w, v in [item.split(": ")]]
    initial_wire_values = {k: v for k, v in initial_wire_values}

    connections = connections.split("\n")

    return initial_wire_values, connections


def part1(data: tuple[dict[str, int], list[str]]) -> int:
    """Solve and return the answer to part 1."""
    wire_values, connections = data

    complete = False
    while not complete:
        tmp_count = 0
        for con in connections:
            w1, op, w2, _, w3 = con.split(" ")
            if w1 in wire_values and w2 in wire_values:
                wire_values[w3] = operations[op](wire_values[w1], wire_values[w2])
                tmp_count += 1

        if tmp_count == len(connections):
            complete = True

    z_keys = reversed(sorted([k for k in wire_values.keys() if k.startswith("z")]))
    result = int("".join(str(wire_values[z]) for z in z_keys), base=2)
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
    puzzle_input = get_data(day=24, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
