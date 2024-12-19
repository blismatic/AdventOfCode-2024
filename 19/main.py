import re
from functools import cache

from aocd import get_data
from dotenv import load_dotenv

with open("19/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> tuple[tuple[str], list[str]]:
    """Parse input."""
    result = puzzle_input.split("\n\n")
    available_towel_patterns = tuple(re.findall(r"\w+", result[0]))
    desired_designs = result[1].split("\n")
    return (available_towel_patterns, desired_designs)


def part1(data: tuple[tuple[str], list[str]]):
    """Solve and return the answer to part 1."""
    available_towel_patterns, desired_designs = data

    def is_possible(design: str, patterns: tuple[str]) -> bool:
        if not design:  # Base case
            return True

        for p in patterns:
            if design.startswith(p):
                if is_possible(design[len(p) :], patterns):
                    return True

        return False  # Fall back

    possible_designs = [d for d in desired_designs if is_possible(d, available_towel_patterns)]

    return len(possible_designs)


def part2(data: tuple[tuple[str], list[str]]):
    """Solve and return the answer to part 2."""
    available_towel_patterns, desired_designs = data

    @cache
    def num_possible_designs(design: str, patterns: tuple[str]) -> bool:
        if not design:  # Base case. An empty design can only be arranged 1 way
            return 1

        count = 0
        for p in patterns:
            if design.startswith(p):
                count += num_possible_designs(design[len(p) :], patterns)

        return count

    results = [num_possible_designs(d, available_towel_patterns) for d in desired_designs]
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
    puzzle_input = get_data(day=19, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
