from enum import Enum
from functools import cache
from itertools import repeat
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


class MachineDefinition(BaseModel):
    button_a_x: int = 0
    button_a_y: int = 0
    button_b_x: int = 0
    button_b_y: int = 0
    prize_x: int = 0
    prize_y: int = 0


def parse_input(input: list[str]) -> list[MachineDefinition]:

    machines: list[MachineDefinition] = []

    current_machine = MachineDefinition()
    for i in range(len(input)):
        if i % 4 == 0:
            numbers = numbers = [int(n) for n in re.findall(r"\d+", input[i])]
            current_machine.button_a_x = numbers[0]
            current_machine.button_a_y = numbers[1]
        elif i % 4 == 1:
            numbers = numbers = [int(n) for n in re.findall(r"\d+", input[i])]
            current_machine.button_b_x = numbers[0]
            current_machine.button_b_y = numbers[1]
        elif i % 4 == 2:
            numbers = numbers = [int(n) for n in re.findall(r"\d+", input[i])]
            current_machine.prize_x = numbers[0]
            current_machine.prize_y = numbers[1]
            machines.append(current_machine)
            current_machine = MachineDefinition()

    return machines


# def solve_machine_movement_iterate(machine: MachineDefinition) -> Tuple[int,int]|None:

#     # to minimize the cost of movement, we will iterate over the value of B,
#     #  stopping when the prize is reachable

#     dbx = machine.prize_x // machine.button_b_x
#     dby = machine.prize_y // machine.button_b_y

#     if dbx==dby and dbx*machine.button_b_x == machine.prize_x and dby*machine.button_b_y == machine.prize_y:
#         return 0, dbx

#     if dbx > dby:
#         b = dbx
#     else:
#         b = dby

#     # print("DBX:", dbx, "DBY:", dby, "B:", b)
#     b+=1
#     while b>0:
#         b-=1

#         bx = b*machine.button_b_x
#         by = b*machine.button_b_y

#         ax = machine.prize_x - bx
#         ay = machine.prize_y - by

#         if ax < 0 or ay < 0:
#             continue

#         dbax = ax // machine.button_a_x
#         dbay = ay // machine.button_a_y

#         if dbax==dbay and dbax*machine.button_a_x == ax and dbay*machine.button_a_y == ay:
#             a = dbax
#             return a,b

#     return None


def solve_machine_movement_2(machine: MachineDefinition) -> Tuple[int, int] | None:
    # pure math solution

    dbx = machine.prize_x // machine.button_b_x
    dby = machine.prize_y // machine.button_b_y

    if (
        dbx == dby
        and dbx * machine.button_b_x == machine.prize_x
        and dby * machine.button_b_y == machine.prize_y
    ):
        return 0, dbx

    b = (
        machine.button_a_x * machine.prize_y - machine.button_a_y * machine.prize_x
    ) / (
        machine.button_a_x * machine.button_b_y
        - machine.button_a_y * machine.button_b_x
    )
    b = int(b)
    a = (machine.prize_x - b * machine.button_b_x) / machine.button_a_x
    a = int(a)

    if (
        a * machine.button_a_x + b * machine.button_b_x == machine.prize_x
        and a * machine.button_a_y + b * machine.button_b_y == machine.prize_y
    ):
        return a, b

    return None


def solve_part1() -> int:

    # 29187

    # input = read_lines("input/day13/example.txt")
    input = read_lines("input/day13/part1.txt")

    machines = parse_input(input)

    total = 0
    for machine in machines:
        # result = solve_machine_movement_iterate(machine)
        result = solve_machine_movement_2(machine)
        # print("Machine:", machine)

        if result is not None:

            cost = 3 * result[0] + result[1]
            # print("A:", result[0], "B:", result[1], "Cost:", cost)
            total += cost

        # else:
        #     print("No solution found")

    return total


def solve_part2() -> int:
    # input = read_lines("input/day13/example.txt")
    input = read_lines("input/day13/part1.txt")

    machines = parse_input(input)

    total = 0
    for machine in machines:
        machine.prize_x += 10000000000000
        machine.prize_y += 10000000000000

        result = solve_machine_movement_2(machine)
        # print("Machine:", machine)

        if result is not None:

            cost = 3 * result[0] + result[1]
            # print("A:", result[0], "B:", result[1], "Cost:", cost)
            total += cost

        # else:
        #     print("No solution found")

    return total
