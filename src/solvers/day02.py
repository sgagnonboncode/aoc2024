from typing import Tuple
from src.common.file_utils import read_lines
import re

def parse_input(lines: list[str]) -> Tuple[list,list]:
    levels:list[list[int]]= []

    for line in lines:
        # extract the numbers from the line using a regular expression
        numbers = re.findall(r"\d+", line)
        if len(numbers) == 0:
            break
        
        levels.append([int(i) for i in numbers])
  
    return levels

def is_safe(row: list[int]) -> bool:
    row_len = len(row)
    
    sign = -1 if row[0] > row[1] else 1
    for i in range(0,row_len-1):
        if sign == -1 and row[i] < row[i+1]:
            return False
        if sign == 1 and row[i] > row[i+1]:
            return False
        
        diff = abs(row[i] - row[i+1])
        if diff > 3:
            return False
        
        if diff < 1:
            return False
        
    return True

def is_safe_with_dampener(row: list[int]) -> bool:
    if is_safe(row):
        return True
    
    # see if we can make it safe by removing one number
    for k in range(0,len(row)):
        row_copy = row.copy()
        row_copy.pop(k)
        if is_safe(row_copy):
            return True

    return False

def solve_part1() -> int:
    lines = read_lines("input/day02/part1.txt")
    # lines = read_lines("input/day02/example.txt")

    levels = parse_input(lines)

    safe_levels = 0
    for row in levels:
        if is_safe(row):
            safe_levels += 1

    return safe_levels

def solve_part2() -> int:
    lines = read_lines("input/day02/part1.txt")
    # lines = read_lines("input/day02/example.txt")

    levels = parse_input(lines)

    safe_levels = 0
    for row in levels:
        if is_safe_with_dampener(row):
            safe_levels += 1

    return safe_levels
