from aocd import get_data
from dotenv import load_dotenv

from pprint import pprint
from collections import defaultdict

example_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse(puzzle_input: str) -> tuple[dict[int, list[int]], list[int]]:
    """Parse input."""
    result = puzzle_input.split("\n\n")
    page_ordering_rules, updates = result
    
    # The right number should be the key, and the left number should become part of a list associated with that key.
    # The values for each key represent what pages must already be present if you want to use the key.
    # For example, { 53: [47, 75, 61, 97] } means that in order to use page 53, pages 47, 75, 61, and 97 must already be present.
    page_ordering_rules = page_ordering_rules.split("\n")
    page_ordering_map = defaultdict(list)
    for rule in page_ordering_rules:
        left, right = rule.split("|")
        page_ordering_map[int(right)].append(int(left))
        
    updates = updates.split("\n")
    updates = [[int(page) for page in update.split(',')] for update in updates]

    # pprint(result[:3])
    print()
    return page_ordering_map, updates

def part1(data):
    """Solve and return the answer to part 1."""
    page_ordering_map, updates = data
    correctly_ordered_updates = []
    
    for update in updates:
        # Remove unnecessary dependencies from the map for this particular update
        temp_page_ordering_map = page_ordering_map.copy()
        for k in temp_page_ordering_map:
            temp_page_ordering_map[k] = [v for v in temp_page_ordering_map[k] if v in update]
        
        # Look at each page in order. If it has no dependencies, or if its dependencies are a subset of the already processed pages, then we are ok.
        # Otherwise, skip processing this update any further.
        already_processed_pages = set()
        skip_update = False
        for page in update:
            if len(temp_page_ordering_map[page]) == 0:
                already_processed_pages.add(page)
            elif (set(temp_page_ordering_map[page]) <= already_processed_pages):
                already_processed_pages.add(page)
            else:
                skip_update = True
                break
            
        if skip_update:
            continue
  
        correctly_ordered_updates.append(update)
    
    middle_page_numbers = [u[len(u)//2] for u in correctly_ordered_updates]
    return sum(middle_page_numbers)


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
    puzzle_input = get_data(day=5, year=2024)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))