from collections import deque
from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("09/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> list[str]:
    """Parse input."""
    result = []

    file_id_counter = 0
    for i, n in enumerate(puzzle_input):
        if i % 2 == 0:
            result.extend([str(file_id_counter)] * int(n))
            file_id_counter += 1
        else:
            result.extend(["."] * int(n))

    pprint(result[:3])
    print()
    return result


def list_rindex(li: list, elem: str) -> int:
    for i in reversed(range(len(li))):
        if li[i] == elem:
            return i
    raise ValueError(f"{elem} not in list.")


def swap(li: list, i1: int, i2: int) -> None:
    li[i1], li[i2] = li[i2], li[i1]


def checksum(li: list[str]) -> int:
    file_blocks = [e for e in li if e != "."]
    result = sum([int(f_id) * i for i, f_id in enumerate(file_blocks)])
    return result


def part1(data: list[str]):
    """Solve and return the answer to part 1."""
    stack = deque([fb for fb in data if fb != "."])
    og_stack_len = len(stack)

    while stack:
        rightmost_fb = stack.pop()
        rightmost_fb_idx = list_rindex(data, rightmost_fb)
        leftmost_freespace_idx = data.index(".")
        if leftmost_freespace_idx >= og_stack_len:
            break
        swap(data, leftmost_freespace_idx, rightmost_fb_idx)

    result = checksum(data)
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
    puzzle_input = get_data(day=9, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
