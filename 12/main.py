from collections import deque
from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

with open("12/example_input.txt", "r") as infile:
    example_input = infile.read()


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")

    height = len(result)
    width = len(result[0])

    grid = {}
    for y in range(height):
        for x in range(width):
            grid[(x, height - y - 1)] = result[y][x]

    pprint(result[:3])
    print()
    return grid


def move(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    dirs = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0), "NE": (1, 1), "SE": (1, -1), "SW": (-1, -1), "NW": (-1, 1)}

    x, y = pos
    dx, dy = dirs[direction]

    return (x + dx, y + dy)


def part1(data: dict[tuple[int, int], str]) -> int:
    """Solve and return the answer to part 1."""
    prices = []

    grid = data.copy()
    already_visited = set()  # This will be a global variable to track which positions we have already processed at some point

    for pos in grid:
        if pos in already_visited:
            continue

        region_area = 0
        region_perimeter = 0
        q = deque()
        q.append(pos)

        # Keep exploring as long as the queue is not empty.
        while q:
            curr_pos = q.pop()
            if curr_pos in already_visited:
                continue
            else:
                already_visited.add(curr_pos)  # Add current position so that we won't ever analyze this position again
                region_area += 1

                neighbors = [move(curr_pos, direction) for direction in ["N", "E", "S", "W"]]
                for n in neighbors:
                    if n in grid and grid[n] == grid[curr_pos]:  # If the neighbor is a valid position *and* of the same plant type
                        q.append(
                            n
                        )  # Add this neighboring position to the queue, so that it will also be explored (since it must be part of the same region)
                    else:
                        region_perimeter += 1

        # After the queue is empty / exhausted, we know that the region's area/perimeter must be fully explored
        region_price = region_area * region_perimeter
        prices.append(region_price)

    result = sum(prices)
    return result


def part2(data):
    """Solve and return the answer to part 2."""

    def is_same_plant(grid: dict[tuple[int, int], str], pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
        if pos1 not in grid or pos2 not in grid:
            return False
        return grid[pos1] == grid[pos2]

    prices = []

    grid = data.copy()
    already_visited = set()

    for pos in grid:
        if pos in already_visited:
            continue

        # print(f"processing the {grid[pos]} region")
        region_area = 0
        region_corners = 0
        q = deque()
        q.append(pos)

        # Keep exploring as long as the queue is not empty.
        while q:
            curr_pos = q.pop()
            curr_plant = grid[curr_pos]
            if curr_pos in already_visited:
                continue

            already_visited.add(curr_pos)  # Add current position so that we wont ever analyze this position again
            region_area += 1
            cardinal_neighbor_positions = [move(curr_pos, direction) for direction in ["N", "E", "S", "W"]]
            for n in cardinal_neighbor_positions:
                if n in grid and grid[n] == grid[curr_pos]:  # If the neighbor is a valid position *and* of the same plant type
                    q.append(n)  # Add this cardinal neighbor to the q so that it will also be analyzed as part of the region

            # * Calculate corners *
            # cardinal_neighbors always in order [N, E, S, W]
            # diag_neighbors always in order [NE, SE, SW, NW]
            cardinal_neighbors = [grid[move(curr_pos, n)] if move(curr_pos, n) in grid else "#" for n in ["N", "E", "S", "W"]]
            diag_neighbors = [grid[move(curr_pos, n)] if move(curr_pos, n) in grid else "#" for n in ["NE", "SE", "SW", "NW"]]
            cardinal_homogenity = [(cn == curr_plant) for cn in cardinal_neighbors]
            diag_homogenity = [(dn == curr_plant) for dn in diag_neighbors]

            # If no cardinal neighbors are of the same type, corners += 4
            if sum(cardinal_homogenity) == 0:
                region_corners += 4

            # If only one cardinal neighbor is of the same type, that position represents 2 corners:
            if sum(cardinal_homogenity) == 1:
                region_corners += 2

            # If two cardinal neighbors are of the same type, then check if the same-neighbors are side by side (N+E, E+S, S+W, or N+W)
            if sum(cardinal_homogenity) == 2:
                if cardinal_homogenity in [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]:
                    region_corners += 1

                    # If side by side were same, check diagonal in that direction. If it is different, that's also an extra corner
                    if (cardinal_homogenity == [1, 1, 0, 0]) and not diag_homogenity[0]:
                        region_corners += 1
                    elif (cardinal_homogenity == [0, 1, 1, 0]) and not diag_homogenity[1]:
                        region_corners += 1
                    elif (cardinal_homogenity == [0, 0, 1, 1]) and not diag_homogenity[2]:
                        region_corners += 1
                    elif (cardinal_homogenity == [1, 0, 0, 1]) and not diag_homogenity[3]:
                        region_corners += 1

            # If three neighbors are same type, check diag neighbors
            if sum(cardinal_homogenity) == 3:
                # NE different, N and E are same
                if (diag_homogenity[0] is False) and (cardinal_homogenity[0] is True and cardinal_homogenity[1] is True):
                    region_corners += 1

                # SE different, E and S are same
                if (diag_homogenity[1] is False) and (cardinal_homogenity[1] is True and cardinal_homogenity[2] is True):
                    region_corners += 1

                # SW different, S and W are same
                if (diag_homogenity[2] is False) and (cardinal_homogenity[2] is True and cardinal_homogenity[3] is True):
                    region_corners += 1

                # NW different, W and N are same
                if (diag_homogenity[3] is False) and (cardinal_homogenity[3] is True and cardinal_homogenity[0] is True):
                    region_corners += 1

            # If four cardinal neighbors are of the same type, then check the diagonal neighbors:
            # Add 1 corner for each diagonal neighbor that is different than the plant
            if sum(cardinal_homogenity) == 4:
                region_corners += sum([1 for dn in diag_neighbors if dn != curr_plant])

        # After the queue is empty, we know that the region has been fully explored
        region_sides = region_corners
        region_price = region_area * region_sides
        prices.append(region_price)

    result = sum(prices)
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
    puzzle_input = get_data(day=12, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
