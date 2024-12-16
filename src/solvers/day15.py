from collections import deque
from enum import Enum
from functools import cache
from itertools import repeat
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


def parse_input(input: list[str]) -> Tuple[list[list[chr]], list[chr], Tuple[int, int]]:

    warehouse_map: list[list[chr]] = []
    robot_instructions: list[chr] = []

    map_mode = True

    robot_x = 0
    robot_y = 0

    for line in input:

        if len(line) <= 1:
            map_mode = False
            continue

        if map_mode:
            warehouse_map.append(list(line[:-1]))

            if "@" in warehouse_map[-1]:
                robot_x = warehouse_map[-1].index("@")
                robot_y = len(warehouse_map) - 1

        else:
            for char in line[:-1]:
                robot_instructions.append(char)

    return warehouse_map, robot_instructions, (robot_x, robot_y)


def get_orientation(instruction: chr) -> Tuple[int, int]:
    if instruction == "^":
        return (0, -1)
    elif instruction == "v":
        return (0, 1)
    elif instruction == "<":
        return (-1, 0)
    elif instruction == ">":
        return (1, 0)
    else:
        return (0, 0)


def robot_step(
    warehouse_map: list[list[chr]],
    robot_position: Tuple[int, int],
    robot_instructions: list[chr],
    i: int,
) -> Tuple[int, int]:
    robot_x, robot_y = robot_position

    movement_orientation = get_orientation(robot_instructions[i])
    if movement_orientation == (0, 0):
        return robot_position

    free = 0
    box = 0
    total = 0

    adjacent_boxes: list[Tuple[int, int]] = []
    box_scan = True

    # scan the direction and count the number of free spaces between the robot and the wall
    if robot_instructions[i] == "^":

        for y in range(robot_y, -1, -1):
            if warehouse_map[y][robot_x] == "#":
                break
            elif warehouse_map[y][robot_x] == ".":
                box_scan = False
                free += 1
            elif warehouse_map[y][robot_x] == "O":
                if box_scan:
                    adjacent_boxes.append((robot_x, y))
                box += 1

            total += 1

    elif robot_instructions[i] == "v":
        for y in range(robot_y, len(warehouse_map)):
            if warehouse_map[y][robot_x] == "#":
                break
            elif warehouse_map[y][robot_x] == ".":
                box_scan = False
                free += 1
            elif warehouse_map[y][robot_x] == "O":
                if box_scan:
                    adjacent_boxes.append((robot_x, y))
                box += 1

            total += 1

    elif robot_instructions[i] == "<":
        for x in range(robot_x, -1, -1):
            if warehouse_map[robot_y][x] == "#":
                break
            elif warehouse_map[robot_y][x] == ".":
                box_scan = False
                free += 1
            elif warehouse_map[robot_y][x] == "O":
                if box_scan:
                    adjacent_boxes.append((x, robot_y))
                box += 1

            if warehouse_map[robot_y][x] != "@":
                total += 1
    elif robot_instructions[i] == ">":
        for x in range(robot_x, len(warehouse_map[0])):
            if warehouse_map[robot_y][x] == "#":
                break
            elif warehouse_map[robot_y][x] == ".":
                box_scan = False
                free += 1
            elif warehouse_map[robot_y][x] == "O":
                if box_scan:
                    adjacent_boxes.append((x, robot_y))
                box += 1

            total += 1
    else:
        return robot_position

    if free > 0:
        adjacent_boxes.reverse()
        for box in adjacent_boxes:
            warehouse_map[box[1] + movement_orientation[1]][
                box[0] + movement_orientation[0]
            ] = "O"

        warehouse_map[robot_y + movement_orientation[1]][
            robot_x + movement_orientation[0]
        ] = "@"
        warehouse_map[robot_y][robot_x] = "."

        return robot_x + movement_orientation[0], robot_y + movement_orientation[1]

    return robot_position


def calculate_gps_value(warehouse_map: list[list[chr]]) -> int:
    total = 0
    for y in range(len(warehouse_map)):
        for x in range(len(warehouse_map[y])):
            if warehouse_map[y][x] in ["O", "["]:
                total += 100 * y + x

    return total


def solve_part1() -> int:

    # 1563092

    # input = read_lines("input/day15/example.txt")
    input = read_lines("input/day15/part1.txt")

    warehouse_map, robot_instructions, position = parse_input(input)

    for i in range(len(robot_instructions)):
        position = robot_step(warehouse_map, position, robot_instructions, i)

    return calculate_gps_value(warehouse_map)


def expand_map(
    warehouse_map: list[list[chr]], robot_position: Tuple[int, int]
) -> Tuple[list[list[chr]], Tuple[int, int]]:

    bigger_map: list[list[chr]] = []

    for y in range(len(warehouse_map)):
        row = []
        for x in range(len(warehouse_map[y])):
            if warehouse_map[y][x] == "#":
                row.append("#")
                row.append("#")
            elif warehouse_map[y][x] == "O":
                row.append("[")
                row.append("]")

            elif warehouse_map[y][x] == ".":
                row.append(".")
                row.append(".")
            elif warehouse_map[y][x] == "@":
                row.append("@")
                row.append(".")
        bigger_map.append(row)

    return bigger_map, (robot_position[0] * 2, robot_position[1])


def big_robot_step2(
    warehouse_map: list[list[chr]], robot_position: Tuple[int, int], instruction: chr
) -> Tuple[int, int]:
    robot_x, robot_y = robot_position

    movement_orientation = get_orientation(instruction)
    if movement_orientation == (0, 0):
        return robot_position

    # next to a wall
    if (
        warehouse_map[robot_y + movement_orientation[1]][
            robot_x + movement_orientation[0]
        ]
        == "#"
    ):
        return robot_position

    # next to empty spot
    if (
        warehouse_map[robot_y + movement_orientation[1]][
            robot_x + movement_orientation[0]
        ]
        == "."
    ):
        warehouse_map[robot_y + movement_orientation[1]][
            robot_x + movement_orientation[0]
        ] = "@"
        warehouse_map[robot_y][robot_x] = "."
        return robot_x + movement_orientation[0], robot_y + movement_orientation[1]

    # next to a box
    # scan adjacent boxes and verify that they can all move

    box_to_verify: deque[Tuple[int, int, int]] = deque()
    box_to_move: list[Tuple[int, int, int]] = []

    horizontal = movement_orientation[0] != 0

    # add the first box
    if horizontal:
        if movement_orientation[0] > 0:
            box_to_verify.append((robot_x + 1, robot_x + 2, robot_y))
            box_to_move.append((robot_x + 1, robot_x + 2, robot_y))
        else:
            box_to_verify.append((robot_x - 2, robot_x - 1, robot_y))
            box_to_move.append((robot_x - 2, robot_x - 1, robot_y))
    else:
        if warehouse_map[robot_y + movement_orientation[1]][robot_x] == "[":
            box_to_verify.append(
                (robot_x, robot_x + 1, robot_y + movement_orientation[1])
            )
            box_to_move.append(
                (robot_x, robot_x + 1, robot_y + movement_orientation[1])
            )
        else:
            box_to_verify.append(
                (robot_x - 1, robot_x, robot_y + movement_orientation[1])
            )
            box_to_move.append(
                (robot_x - 1, robot_x, robot_y + movement_orientation[1])
            )

    # test all adjacent
    while len(box_to_verify) > 0:
        box = box_to_verify.pop()

        if horizontal:

            if movement_orientation[0] > 0:
                hadj = (box[1] + 1, box[1] + 2, box[2])
            else:
                hadj = (box[0] - 2, box[0] - 1, box[2])

            ajdidx = 0 if movement_orientation[0] > 0 else 1

            if warehouse_map[hadj[2]][hadj[ajdidx]] == ".":
                # this box can move right
                continue
            elif warehouse_map[hadj[2]][hadj[ajdidx]] == "#":
                # this box cannot move right => robot stuck
                return robot_position

            elif warehouse_map[hadj[2]][hadj[ajdidx]] in ["[", "]"]:
                # adjacent to another box , add it to the list if we havent seen it yet
                if not (hadj[1], hadj[1], hadj[2]) in box_to_move:
                    box_to_verify.append((hadj[0], hadj[1], hadj[2]))
                    box_to_move.append((hadj[0], hadj[1], hadj[2]))

        else:
            # vertical
            if (
                warehouse_map[box[2] + movement_orientation[1]][box[0]] == "."
                and warehouse_map[box[2] + movement_orientation[1]][box[1]] == "."
            ):
                # this box can move down
                continue
            if (
                warehouse_map[box[2] + movement_orientation[1]][box[0]] == "#"
                or warehouse_map[box[2] + movement_orientation[1]][box[1]] == "#"
            ):
                # this box cannot move down => robot stuck
                return robot_position

            if warehouse_map[box[2] + movement_orientation[1]][box[1]] == "[":
                # skew right
                if (
                    not (box[0] + 1, box[1] + 1, box[2] + movement_orientation[1])
                    in box_to_move
                ):
                    box_to_verify.append(
                        (box[0] + 1, box[1] + 1, box[2] + movement_orientation[1])
                    )
                    box_to_move.append(
                        (box[0] + 1, box[1] + 1, box[2] + movement_orientation[1])
                    )

            if warehouse_map[box[2] + movement_orientation[1]][box[0]] == "]":
                # skew left
                if (
                    not (box[0] - 1, box[1] - 1, box[2] + movement_orientation[1])
                    in box_to_move
                ):
                    box_to_verify.append(
                        (box[0] - 1, box[1] - 1, box[2] + movement_orientation[1])
                    )
                    box_to_move.append(
                        (box[0] - 1, box[1] - 1, box[2] + movement_orientation[1])
                    )

            if (
                warehouse_map[box[2] + movement_orientation[1]][box[0]] == "["
                and warehouse_map[box[2] + movement_orientation[1]][box[1]] == "]"
            ):
                # inline
                if (
                    not (box[0], box[1], box[2] + movement_orientation[1])
                    in box_to_move
                ):
                    box_to_verify.append(
                        (box[0], box[1], box[2] + movement_orientation[1])
                    )
                    box_to_move.append(
                        (box[0], box[1], box[2] + movement_orientation[1])
                    )

    # clean the previous positions of the boxes
    for box in box_to_move:
        warehouse_map[box[2]][box[0]] = "."
        warehouse_map[box[2]][box[1]] = "."

    # move the boxes
    for box in box_to_move:
        warehouse_map[box[2] + movement_orientation[1]][
            box[0] + movement_orientation[0]
        ] = "["
        warehouse_map[box[2] + movement_orientation[1]][
            box[1] + movement_orientation[0]
        ] = "]"

    # move the robot
    warehouse_map[robot_y + movement_orientation[1]][
        robot_x + movement_orientation[0]
    ] = "@"
    warehouse_map[robot_y][robot_x] = "."

    return robot_x + movement_orientation[0], robot_y + movement_orientation[1]


def print_bigger_map(bigger_map: list[list[chr]]) -> None:
    for y in range(len(bigger_map)):
        print("".join(bigger_map[y]))
    print()


def solve_part2() -> int:

    # 1582688

    # input = read_lines("input/day15/example.txt")
    input = read_lines("input/day15/part1.txt")

    warehouse_map, robot_instructions, position = parse_input(input)
    bigger_map, position = expand_map(warehouse_map, position)

    for i in range(len(robot_instructions)):
        position = big_robot_step2(bigger_map, position, robot_instructions[i])

    return calculate_gps_value(bigger_map)
