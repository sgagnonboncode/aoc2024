from enum import Enum
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


class Equation:

    def __init__(self, equation: str):
        raw_numbers = re.findall(r"\d+", equation)
        self.answer = int(raw_numbers[0])
        self.numbers = [int(n) for n in raw_numbers[1:]]

    def try_solve_part_1(self) -> bool:
        # guide a brute force solution by ensuring that the calculation space number is never higher than the answer
        # since we only add or multiply , the equation is a monotonic increasing function

        # solutions will be represented as a bitwize number with 0 being 'add' and '1' being multiply
        op_count = len(self.numbers) - 1
        num_solution = 2**op_count

        for i in range(num_solution):

            current = self.numbers[0]

            for j in range(op_count):
                if i & (1 << j):
                    current *= self.numbers[j + 1]
                else:
                    current += self.numbers[j + 1]

                if current > self.answer:
                    break

            if current == self.answer:
                return True

        return False

    def try_solve_part_2(self) -> bool:
        # no point in solving for || operator if part 1 already produced a solution
        # part 1 being very fast, we can afford to do this check
        if self.try_solve_part_1():
            return True

        # same as part 1 , but now with 3 operators (modulo instead of bitwize):  0 = add, 1 = multiply, 2 = aggregate
        op_count = len(self.numbers) - 1
        num_solution = 3**op_count

        # start from 2 since we already tried part 1 (0 and 1 are already covered)
        # we could probably cull even more solutions by checking if the aggregate operator is used
        #  at least once but this is good enough for my cpu. (Ryzen 5800x)
        for i in range(2, num_solution):
            current = self.numbers[0]
            remaining_operators = i

            for j in range(op_count):
                cur_op = remaining_operators % 3
                remaining_operators = remaining_operators // 3

                if cur_op == 0:
                    current += self.numbers[j + 1]
                elif cur_op == 1:
                    current *= self.numbers[j + 1]
                else:
                    # aggregate
                    current = int(f"{current}{self.numbers[j+1]}")

                if current > self.answer:
                    break

            if current == self.answer:
                return True

        return False


def solve_part1() -> int:
    # lines = read_lines("input/day07/example.txt")
    lines = read_lines("input/day07/part1.txt")

    total = 0

    for line in lines:
        if len(line) == 0:
            continue

        equation = Equation(line)
        if equation.try_solve_part_1():
            total += equation.answer

    return total


def solve_line(line: str) -> int:
    if len(line) == 0:
        return 0

    equation = Equation(line)
    if equation.try_solve_part_2():
        return equation.answer

    return 0


def solve_part2() -> int:
    # lines = read_lines("input/day07/example.txt")
    lines = read_lines("input/day07/part1.txt")

    total = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for line_total in zip(lines, executor.map(solve_line, lines)):
            total += line_total[1]

    return total
