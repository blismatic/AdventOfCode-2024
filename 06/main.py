from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint

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
    result = ['X' + row + 'X' for row in result] # Add padding to left and right column
    result.insert(0, 'X'*len(result[0])) # Add padding to top
    result.append('X'* len(result[0])) # Add padding to bottom
    
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

def move(curr_pos: tuple[int, int], dxy: tuple[int, int]) -> tuple[int, int]:
    x, y = curr_pos
    dx, dy = dxy
    return (x+dx, y+dy)

def part1(data):
    """Solve and return the answer to part 1."""
    grid = data
    guard_pos = get_guard_position(data)
    
    # indexes 0, 1, 2, 3 map to cardinal directions N, E, S, W (turning to the right each time)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    # if the tuples look wrong, keep in mind that (0, 0) is the top left of our grid, and it expands to the bottom right
    
    curr_pos = guard_pos
    curr_direction = directions[0]
    unique_positions = set() # This will be a set of 2-tuple coordinate pairs that have been visited
    
    while grid[curr_pos] != 'X': # X is the border we padded around our entire room
        unique_positions.add(curr_pos)
        tmp_curr_pos = move(curr_pos, dxy=curr_direction) # This is temporary because we might not use it if we would have stepped on an obstacle
        if grid[tmp_curr_pos] == '#':
            curr_direction = directions[(directions.index(curr_direction)+1)%len(directions)] # Turn to the right
            continue
        else:
            curr_pos = tmp_curr_pos
            
    return len(unique_positions)
        
        
    


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
    puzzle_input = get_data(day=6, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))