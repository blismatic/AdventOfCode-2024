from collections import deque
from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("09/example_input.txt", "r") as infile:
    example_input = infile.read()
# 00...111...2...333.44.5555.6666.777.888899


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


def swap(li: list, i1: int, i2: int, n: int) -> None:
    for x in range(n):
        li[i1 + x], li[i2 + x] = li[i2 + x], li[i1 + x]


def checksum(li: list[str]) -> int:
    # file_blocks = [e for e in li if e != "."]
    result = sum([int(f_id) * i for i, f_id in enumerate(li) if f_id != "."])
    return result


def peek(stack: deque) -> str:
    if len(stack) == 0:
        return None
    elem = stack.pop()
    stack.append(elem)
    return elem


def find_contiguous_free_space(li: list[str], n: int) -> int | None:
    """Returns the first index of a block of contiguous space of size n. Returns None if not found."""
    count = 0
    for i, char in enumerate(li):
        if char == ".":
            count += 1
            if count == n:
                return i - n + 1
        else:
            count = 0
    return None


def part1(data: list[str]):
    """Solve and return the answer to part 1."""
    d = data.copy()
    stack = deque([fb for fb in d if fb != "."])
    og_stack_len = len(stack)

    while stack:
        rightmost_fb = stack.pop()
        rightmost_fb_idx = list_rindex(d, rightmost_fb)
        leftmost_freespace_idx = d.index(".")
        if leftmost_freespace_idx >= og_stack_len:
            break
        swap(d, leftmost_freespace_idx, rightmost_fb_idx, 1)

    result = checksum(d)
    return result


def part2(data: list[str]):
    """Solve and return the answer to part 2."""
    d = data.copy()
    stack = deque([fb for fb in d if fb != "."])
    while stack:
        curr_top = stack.pop()
        full_file_block = [curr_top]
        while peek(stack) == curr_top:
            full_file_block.append(stack.pop())

        full_file_block_start_idx = d.index(full_file_block[0])
        free_space_idx = find_contiguous_free_space(d, len(full_file_block))
        if (free_space_idx is not None) and (free_space_idx < full_file_block_start_idx):
            swap(d, free_space_idx, full_file_block_start_idx, len(full_file_block))

    result = checksum(d)
    return result


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
