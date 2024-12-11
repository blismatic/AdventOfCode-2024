from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("11/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split(" ")

    pprint(result[:10])
    print()
    return result


def blink(stones: list[str]) -> list[str]:
    # Rule 1: if the stone is 0, it becomes 1
    # Rule 2: if the stone has an even number of digits, it is replaced by two stones.
    #         the left half of digits are on the left stone, and
    #         the right half of digits are on the right stone.
    #         Neither half keeps leading zeroes (e.g. 1000 -> 10 and 0)
    # Rule 3: If rule 1 or 2 does not apply, the new stone is the old number * 2024
    new_stones = []
    for s in stones:
        if s == "0":
            new_stones.append("1")
        elif len(s) % 2 == 0:
            left = int(s[: len(s) // 2])
            right = int(s[len(s) // 2 :])
            new_stones.extend([str(left), str(right)])
        else:
            new_stones.append(str(int(s) * 2024))
    return new_stones


def part1(data: list[str]):
    """Solve and return the answer to part 1."""
    d = data.copy()
    for _ in range(25):
        d = blink(d)

    return len(d)


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
    puzzle_input = get_data(day=11, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
