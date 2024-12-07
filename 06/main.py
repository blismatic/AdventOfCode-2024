from pprint import pprint

from aocd import get_data
from dotenv import load_dotenv

example_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")
    result = ["X" + row + "X" for row in result]  # Add padding to left and right column
    result.insert(0, "X" * len(result[0]))  # Add padding to top
    result.append("X" * len(result[0]))  # Add padding to bottom

    grid = {}
    for y in range(len(result)):
        for x in range(len(result[0])):
            grid[(x, y)] = result[y][x]

    pprint(result[:3])
    print()
    return grid


def get_guard_position(room: dict[tuple[int, int], str]) -> tuple[int, int]:
    for k, v in room.items():
        if v == "^":
            return k
    raise LookupError("could not find the guard (^) in the room")


def move(curr_pos: tuple[int, int], direction: str) -> tuple[int, int]:
    x, y = curr_pos
    directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    if direction not in directions:
        raise ValueError("direction parameter must be one of: N, E, S, W")

    dx, dy = directions[direction]
    return (x + dx, y + dy)

def place_obstacle(grid: dict[tuple[int, int], str], obstacle_pos: tuple[int, int]) -> dict[tuple[int, int], str]:
    grid_copy = grid.copy()
    grid_copy[obstacle_pos] = "#"
    return grid_copy

def print_grid(grid: dict[tuple[int, int], str], guard_pos_direction = tuple[int, int, str]) -> None:
    direction_symbols = {
        "N": "^",
        "E": ">",
        "S": "v",
        "W": "<"
    }
    
    grid_copy = grid.copy()
    guard_x, guard_y, direction = guard_pos_direction
    grid_copy[(guard_x, guard_y)] = direction_symbols[direction]
    
    max_x = max(key[0] for key in grid_copy)
    max_y = max(key[1] for key in grid_copy)

    # Print each row of the grid
    for y in range(max_y + 1):
        row = ''.join(grid_copy.get((x, y), ' ') for x in range(max_x + 1))
        print(row)


def part1(data):
    """Solve and return the answer to part 1."""
    grid = data
    guard_pos = get_guard_position(grid)

    # indexes 0, 1, 2, 3 map to cardinal directions N, E, S, W (turning to the right each time)
    # directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    directions = ["N", "E", "S", "W"]
    # if the tuples look wrong, keep in mind that (0, 0) is the top left of our grid, and it expands to the bottom right

    curr_pos = guard_pos
    curr_direction = directions[0]
    unique_positions = set()  # This will be a set of 2-tuple coordinate pairs that have been visited

    while grid[curr_pos] != "X":  # X is the border we padded around our entire room
        unique_positions.add(curr_pos)
        tmp_curr_pos = move(curr_pos, curr_direction)  # This is temporary because we might not use it if we would have stepped on an obstacle
        if grid[tmp_curr_pos] == "#":
            curr_direction = directions[(directions.index(curr_direction) + 1) % 4]  # Turn to the right
            continue
        else:
            curr_pos = tmp_curr_pos

    return len(unique_positions)


def part2(data):
    """Solve and return the answer to part 2."""
    grid = data
    guard_pos = get_guard_position(grid)
    directions = ["N", "E", "S", "W"]

    # First establish the unique positions that the guard will step over normally so that you have your possible obstacle locations
    curr_pos = guard_pos
    curr_direction = directions[0]
    original_path_unique_positions = set()

    while grid[curr_pos] != "X":
        original_path_unique_positions.add(curr_pos)
        ghost_pos = move(
            curr_pos, curr_direction
        )  # This is a ghost in the sense that it's not actually where we are right now, it's where we *might* be on the next step
        if grid[ghost_pos] == "#":
            curr_direction = directions[(directions.index(curr_direction) + 1) % 4]  # Turn to the right
            continue
        else:
            curr_pos = ghost_pos

    # Using the original path positions, try to place an obstacle at each one and then re-run the simulation.
    # However, this time, keep track of the unique positions *and* the direction the guard was facing at that position
    # This will be a set of 3-tuples consisting of (x, y, direction) where direction is either "N", "E", "S", "W"
    # The simulation should loop as long as the current position is not a "#", with a True/False flag for `loop_detected` that starts off as false
    # If the simulation ends as a result of the current position being on an "X", then that obstacle location did not result in a loop
    # If the simulation ends as a result of coming across the same (x, y, direction), then you know that there *was* a loop
    obstacle_positions_that_cause_loops = set()
    for p in original_path_unique_positions:
        if p == guard_pos:
            continue # Skip the guards starting position, since you can't place an obstacle there.
        
        new_grid = place_obstacle(grid, p)
        curr_pos: tuple[int, int] = guard_pos
        curr_direction = directions[0]
        unique_positions_directions = set()
        
        loop_detected = False
        while new_grid[curr_pos] != "X":
            unique_positions_directions.add(curr_pos + (curr_direction,))
            ghost_pos = move(curr_pos, curr_direction)
            if new_grid[ghost_pos] == "#":
                curr_direction = directions[(directions.index(curr_direction) + 1) % 4]
                continue
            elif (ghost_pos + (curr_direction,)) in unique_positions_directions:
                loop_detected = True
                break
            else:
                curr_pos = ghost_pos
                
        if loop_detected:
            obstacle_positions_that_cause_loops.add(p)
            
    return len(obstacle_positions_that_cause_loops)
            


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=6, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))
