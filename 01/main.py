from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint
from collections import Counter

example_input = """"""


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")
    left_list = [int(row.split("   ")[0]) for row in result]
    right_list = [int(row.split("   ")[1]) for row in result]
    left_list.sort()
    right_list.sort()

    pprint(result[:3])
    print()
    return left_list, right_list


def part1(data):
    """Solve and return the answer to part 1."""
    distances = [abs(left_num - right_num) for left_num, right_num in zip(*data)]
    return sum(distances)


def part2(data):
    """Solve and return the answer to part 2."""
    left_list, right_list = data
    
    right_counter = Counter(right_list)
    similarity_scores = [(left_num * right_counter.get(left_num, 0)) for left_num in left_list]
        
    return sum(similarity_scores)


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=1, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))