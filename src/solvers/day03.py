from typing import Tuple
from src.common.file_utils import read_lines
import re


def solve_part1() -> int:
    lines = read_lines("input/day03/part1.txt")
    # lines = read_lines("input/day02/example.txt")

    total = 0

    for line in lines:
        sequences = re.findall(r"mul\(\d+,\d+\)", line)

        for sequence in sequences:
            numbers = re.findall(r"\d+", sequence)
            total += int(numbers[0]) * int(numbers[1])

    return total

def solve_part2() -> int:
    lines = read_lines("input/day03/part1.txt")
    # lines = read_lines("input/day02/example.txt")

    total = 0
    mul_active = True

    for line in lines:
        sequences = re.findall(r"(mul\(\d+,\d+\)|do\(\)|don't\(\))", line)

        for sequence in sequences:

            if sequence == "do()":
                mul_active = True
                continue

            if sequence == "don't()":
                mul_active = False
                continue

            if mul_active:
                numbers = re.findall(r"\d+", sequence)
                total += int(numbers[0]) * int(numbers[1])

    return total
