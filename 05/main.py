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

def group_updates(mapping: defaultdict, updates: list[list[int]]) -> tuple[list[int], list[int]]:
    correctly_ordered = []
    incorrectly_ordered = []
    
    for update in updates:
        # Remove unnecessary dependencies from the map for this particular update
        temp_mapping = mapping.copy()
        for key, value in temp_mapping.items():
            temp_mapping[key] = [v for v in value if v in update]
            
        # Look at each page in order. 
        # # If the page has no dependencies, or if its dependencies are a subset of the already processed pages, then keep processing it
        # # If there is something wrong with the dependencies, group it in `incorrectly_ordered` and break out
        # # If you get to the end of the update, group it in `correctly_ordered`
        already_processed_pages = set()
        skip_update = False
        for page in update:
            if len(temp_mapping[page]) == 0:
                already_processed_pages.add(page)
            elif (set(temp_mapping[page]) <= already_processed_pages):
                already_processed_pages.add(page)
            else:
                skip_update = True
                break
            
        if skip_update:
            incorrectly_ordered.append(update)
        else:
            correctly_ordered.append(update)
    
    return correctly_ordered, incorrectly_ordered

def fix_update(mapping: defaultdict, update: list[int]) -> list[int | None]:
    """Attempt to fix an update according to certain page rules"""
    # 75,97,47,61,53 becomes 97,75,47,61,53
    # 61,13,29 becomes 61,29,13
    # 97,13,75,29,47 becomes 97,75,47,29,13
    
    # Remove unnecessary dependencies from the map for this particular update
    temp_mapping = mapping.copy()
    for key, value in temp_mapping.items():
        temp_mapping[key] = [v for v in value if v in update]
        
    already_processed_pages = set()
    for i, page in enumerate(update):
        if len(temp_mapping[page]) == 0:
            already_processed_pages.add(page)
        elif (set(temp_mapping[page]) <= already_processed_pages):
            already_processed_pages.add(page)
        else:
            # swap and try again
            temp_update = update.copy()
            temp_update[i], temp_update[(i+1)%len(temp_update)] = temp_update[(i+1)%len(temp_update)], temp_update[i]
            return fix_update(mapping, temp_update)
    
    return update
    

def part1(data):
    """Solve and return the answer to part 1.""" 
    correctly_ordered_updates, _ = group_updates(*data)
    
    middle_page_numbers = [u[len(u)//2] for u in correctly_ordered_updates]
    return sum(middle_page_numbers)


def part2(data):
    """Solve and return the answer to part 2."""
    page_ordering_map, updates = data
    _, incorrectly_ordered_updates = group_updates(page_ordering_map, updates)
    
    fixed_updates = [fix_update(page_ordering_map, u) for u in incorrectly_ordered_updates]
    
    middle_page_numbers = [u[len(u)//2] for u in fixed_updates]
    return sum(middle_page_numbers)


def solve(puzzle_input) -> tuple:
    """Solve the puzzle for the given input. Returns a tuple containing the answers to part 1 and part 2."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    load_dotenv()
    solutions = solve(example_input)
    puzzle_input = get_data(day=5, year=2024)
    # solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))