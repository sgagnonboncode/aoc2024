from typing import Tuple
from src.common.file_utils import read_lines
import re

def parse_input(lines: list[str]) -> Tuple[list,list]:
    left:list[int]= []
    right: list[int] = []

    for line in lines:
        # extract the numbers from the line using a regular expression
        numbers = re.findall(r"\d+", line)

        if len(numbers) != 2:
            break

        left.append(int(numbers[0]))
        right.append(int(numbers[1]))

    return (left, right)

def solve_part1() -> int:
    lines = read_lines("input/day01/part1.txt")
    left, right = parse_input(lines)

    sorted_left = sorted(left)
    sorted_right = sorted(right)

    total =0
    for i in range(0,len(sorted_left)):
        distance = abs(sorted_left[i] - sorted_right[i])
        total += distance

    return total

def solve_part2() -> int:
    lines = read_lines("input/day01/part1.txt")
    left, right = parse_input(lines)

    total = 0
    for i in range(0,len(left)):
        number = left[i]
        occurences = right.count(number)
        total += number*occurences

    return total
