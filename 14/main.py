import copy
import os
import re
import statistics
from collections import defaultdict
from pprint import pprint
from typing import TypeAlias

import keyboard
from aocd import get_data
from dotenv import load_dotenv

Grid: TypeAlias = dict[tuple[int, int], list[tuple[int, int]]]
HEIGHT = 103
WIDTH = 101

with open("14/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str) -> Grid:
    """Parse input."""
    result = puzzle_input.split("\n")

    grid = defaultdict(list)

    for line in result:
        position, velocity = line.split(" ")
        px, py = re.findall(r"-?\d+", position)
        vx, vy = re.findall(r"-?\d+", velocity)
        grid[(int(px), int(py))].append((int(vx), int(vy)))

    pprint(result[:3])
    print()
    return grid


def simulate(g: Grid, n: int = 1, backwards: bool = False) -> Grid:
    new_grid = defaultdict(list)

    for pos in g:
        px, py = pos
        robots = g[pos]

        for r in robots:
            vx, vy = r
            if backwards:
                new_x = (px - (vx * n)) % WIDTH
                new_y = (py - (vy * n)) % HEIGHT
            else:
                new_x = (px + (vx * n)) % WIDTH
                new_y = (py + (vy * n)) % HEIGHT

            new_grid[(new_x, new_y)].append((vx, vy))

    return new_grid


def view_grid(g: Grid) -> None:
    new_g = copy.deepcopy(g)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            char = len(new_g[(x, y)])
            if char == 0:
                char = "."
            print(char, end="")
        print("", end="\n")


def split_into_quadrants(g: Grid) -> list[Grid]:
    middle_column = WIDTH // 2
    middle_row = HEIGHT // 2

    top_left = defaultdict(list)
    top_right = defaultdict(list)
    bot_left = defaultdict(list)
    bot_right = defaultdict(list)

    for pos in g:
        px, py = pos
        if px < middle_column and py < middle_row:
            top_left[pos] = g[pos]
        elif px > middle_column and py < middle_row:
            top_right[pos] = g[pos]
        elif px < middle_column and py > middle_row:
            bot_left[pos] = g[pos]
        elif px > middle_column and py > middle_row:
            bot_right[pos] = g[pos]

    return [top_left, top_right, bot_left, bot_right]


def part1(data: Grid):
    """Solve and return the answer to part 1."""
    x = simulate(data, n=100)

    quadrants = split_into_quadrants(x)
    robots_per_quadrant = [sum([len(robots) for pos, robots in q.items()]) for q in quadrants]

    safety_factor = 1
    for n in robots_per_quadrant:
        safety_factor *= n

    return safety_factor


def part2(data: Grid):
    """Solve and return the answer to part 2."""

    def get_stdev(g: Grid) -> tuple[float, float]:
        x_stdev = statistics.stdev([x for x, y in g.keys()])
        y_stdev = statistics.stdev([y for x, y in g.keys()])
        return (x_stdev, y_stdev)

    x_stdev, y_stdev = get_stdev(data)
    THRESHOLD = 28  # Fine tune this number
    counter = 0

    try:
        print("Press the '.' key on your keyboard to begin searching for the christmas tree.")
        while True:
            if keyboard.is_pressed("."):
                while (x_stdev > THRESHOLD) or (y_stdev > THRESHOLD):
                    counter += 1
                    data = simulate(data)
                    x_stdev, y_stdev = get_stdev(data)
                os.system("cls")
                view_grid(data)
                print(f"{x_stdev=}, {y_stdev=}")
                print("Press 'q' if you see the christmas tree. Otherwise, press '.' to continue searching.")
                x_stdev, y_stdev = (THRESHOLD * 2, THRESHOLD * 2)  # Reset standard deviation
            elif keyboard.is_pressed("q"):
                raise KeyboardInterrupt()
    except KeyboardInterrupt:
        os.system("cls")

    return counter


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=14, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
