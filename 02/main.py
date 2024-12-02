from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint

example_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")
    result = [[int(level) for level in report.split()] for report in result]

    pprint(result[:3])
    print()
    return result

def safe(report: list[int]) -> bool:
    is_ascending = True if (report[1] - report[0]) > 0 else False
    prev_level = report[0]
    
    for level in report[1:]:
        distance = level - prev_level
        if is_ascending and distance not in [1, 2, 3]:
            return False
        elif not is_ascending and distance not in [-1, -2, -3]:
            return False
        
        prev_level = level
    return True

def part1(data):
    """Solve and return the answer to part 1."""
    result = [safe(report) for report in data]
    return sum(result)


def part2(data):
    """Solve and return the answer to part 2."""
    result = []
    for report in data:
        variations = [report[:i] + report[i+1:] for i in range(len(report))]
        result.append(True) if any([safe(v) for v in variations]) else result.append(False)
    return sum(result)


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=2, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))