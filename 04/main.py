from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint

example_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def parse(puzzle_input: str):
    """Parse input."""
    result = puzzle_input.split("\n")

    pprint(result[:3])
    print()
    return result

def check_neighbor(grid: list[str], x: int, y: int, dx: int, dy: int) -> str:    
    max_x = len(grid[0])
    max_y = len(grid)
    
    if not (0 <= (x + dx) < max_x):
        return '.'
    elif not (0 <= (y + dy) < max_y):
        return '.'
    
    try:
        neighbor = grid[y+dy][x+dx]
        return neighbor
    except IndexError:
        return '.'

def part1(data):
    """Solve and return the answer to part 1."""
    directions = {
        "N":  (0, -1),
        "NE": (1, -1),
        "E":  (1, 0),
        "SE": (1, 1),
        "S":  (0, 1),
        "SW": (-1, 1),
        "W":  (-1, 0),
        "NW": (-1, -1)
    }
    
    total_xmas_occurences = 0
    
    for y in range(len(data)):
        for x in range(len(data[0])):
            char = data[y][x]
            
            if char != 'X':
                continue
            
            for direction in directions.values():
                dx, dy = direction
                curr_x = x
                curr_y = y
                temp_string = 'X'
                for _ in range(3):
                    temp_string += check_neighbor(data, curr_x, curr_y, dx, dy)
                    curr_x += dx
                    curr_y += dy
                    
                if temp_string == 'XMAS':
                    total_xmas_occurences += 1
    
    return total_xmas_occurences

def part2(data):
    """Solve and return the answer to part 2."""
    directions = {
        "NE": (1, -1),
        "SE": (1, 1),
        "SW": (-1, 1),
        "NW": (-1, -1)
    }
    
    total_x_mas_occurences = 0
    
    for y in range(len(data)):
        for x in range(len(data[0])):
            char = data[y][x]
            
            if char != 'A':
                continue
            
            TR_BR_BL_TL = []
            for direction in directions.values():
                dx, dy = direction
                TR_BR_BL_TL.append(check_neighbor(data, x, y, dx, dy))

            if any([char in ['X', '.', 'A'] for char in TR_BR_BL_TL]):
                continue
            
            TR, BR, BL, TL = TR_BR_BL_TL
            if (TR != BL) and (BR != TL):
                # If the diagonals have different characters, we know it is good.
                total_x_mas_occurences += 1
    
    return total_x_mas_occurences


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    # solutions = solve(example_input)
    puzzle_input = get_data(day=4, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))