from enum import Enum
from functools import cache
from itertools import repeat
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


# part 1 , hard simulation of the blink logic as described in the problem
def simulate_blink_step(input: list[int]):

    result = []

    for i in range(0, len(input)):

        # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        if input[i] == 0:
            result.append(1)

        # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
        #   The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone.
        #   (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
        elif len(str(input[i])) % 2 == 0:
            s = str(input[i])
            result.append(int(s[0 : len(s) // 2]))
            result.append(int(s[len(s) // 2 :]))

        # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
        else:
            result.append(input[i] * 2024)

    return result


# part 2 , simplified / memoizable version of the blink logic as described in the problem
@cache
def simulate_blink_logic(input: int) -> list[int]:
    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if input == 0:
        return [1]

    s = str(input)
    len_input = len(s)

    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
    #   The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone.
    #   (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    if len_input % 2 == 0:
        return [int(s[0 : len_input // 2]), int(s[len_input // 2 :])]

    # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    return [input * 2024]


def solve_part1() -> int:
    # input = read_lines("input/day11/example.txt")
    input = read_lines("input/day11/part1.txt")
    numbers = [int(n) for n in re.findall(r"\d+", input[0])]

    for i in range(25):
        numbers = simulate_blink_step(numbers)

    return len(numbers)


def solve_part2() -> int:
    # input = read_lines("input/day11/example.txt")
    input = read_lines("input/day11/part1.txt")
    numbers = [int(n) for n in re.findall(r"\d+", input[0])]

    # since the number of states involed in 75 blinks is too large, we will simplify
    # the problem.
    # firstly, every number can be evaluated independently of the others since they
    #   never interact with each other.
    # secondly, since the result for a given number will never change, no matter where it is
    #   located, we can simplify the calculation by combining all of the numbers into a dictionary.
    #   the sequence length is what matter for this problem , so we can ignore the actual sequence
    # using these two simplifications, we can calculate the result for each individual number and the
    #   resulting length of sequence at the end.
    # a @cache decorator is used to enable memoization for the function simulate_blink_logic

    total = 0
    for n in numbers:
        number_results = {n: 1}
        for step in range(75):
            numbers_next = {}
            for k, v in number_results.items():
                for r in simulate_blink_logic(k):
                    numbers_next.setdefault(r, 0)
                    numbers_next[r] += v

            number_results = numbers_next

        total += sum([v for k, v in number_results.items()])

    return total
