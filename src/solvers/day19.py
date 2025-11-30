from src.common.file_utils import read_lines
from functools import cache

def find_solutions(towel_patterns: list[str], complex_pattern: str) -> int:
        
    # using memoization, function is nested to create a closure
    # over tower_patterns and complex_pattern
    @cache
    def count_solutions(current:str) -> int:
        nb_solutions =0
        for towel_pattern in towel_patterns:
            # see if we can append the towel to the start of the complex pattern
            combo = current+towel_pattern

            # if the pattern is formed, add it to the count
            if combo == complex_pattern:
                nb_solutions+=1
            elif complex_pattern.startswith(combo):
                # if the combo is possible , keep searching
                nb_solutions += count_solutions(combo)

        return nb_solutions
    
    return count_solutions("")

def solve_part1() -> int:
    # input_lines = read_lines("input/day19/example.txt")
    input_lines = read_lines("input/day19/part1.txt")
    
    towel_patterns = [towel_pattern.strip() for towel_pattern in input_lines[0].split(",")]
    complex_patterns = [l.strip() for l in input_lines[2:]]
    
    return sum([1 for complex_pattern in complex_patterns if find_solutions(towel_patterns, complex_pattern) > 0])

def solve_part2() -> int:
    # input_lines = read_lines("input/day19/example.txt")
    input_lines = read_lines("input/day19/part1.txt")
    
    towel_patterns = [towel_pattern.strip() for towel_pattern in input_lines[0].split(",")]
    complex_patterns = [l.strip() for l in input_lines[2:]]
    
    possibilities = 0
    for complex_pattern in complex_patterns:
        current_pattern = find_solutions(towel_patterns, complex_pattern)
        # print(f"Pattern {complex_pattern} can be formed in {current_pattern} ways.")
        possibilities += current_pattern

    return sum([find_solutions(towel_patterns, complex_pattern) for complex_pattern in complex_patterns])