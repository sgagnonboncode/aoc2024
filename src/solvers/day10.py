from enum import Enum
from itertools import repeat
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


def parse_map(input: list[str]) -> list[list[int]]:

    trail_map = []

    for line in input:
        numbers = [int(n) for n in re.findall(r"\d", line)]
        if len(numbers) > 0:
            trail_map.append(numbers)

    return trail_map


def traverse_map(
    x: int,
    y: int,
    x_size: int,
    y_size: int,
    trail_map: list[list[int]],
    trail_heads: set[Tuple[int, int]],
):

    if x >= x_size or y >= y_size or x < 0 or y < 0:
        return

    current_height = trail_map[y][x]
    if current_height == 9:
        trail_heads.add((x, y))
        return

    # top
    if y > 0 and trail_map[y - 1][x] == current_height + 1:
        traverse_map(x, y - 1, x_size, y_size, trail_map, trail_heads)

    # bottom
    if y < y_size - 1 and trail_map[y + 1][x] == current_height + 1:
        traverse_map(x, y + 1, x_size, y_size, trail_map, trail_heads)

    # left
    if x > 0 and trail_map[y][x - 1] == current_height + 1:
        traverse_map(x - 1, y, x_size, y_size, trail_map, trail_heads)

    # right
    if x < x_size - 1 and trail_map[y][x + 1] == current_height + 1:
        traverse_map(x + 1, y, x_size, y_size, trail_map, trail_heads)


def traverse_map_part2(
    x: int,
    y: int,
    x_size: int,
    y_size: int,
    current_path: list[Tuple[int, int]],
    trail_map: list[list[int]],
    trail_paths: list[Tuple[int, int]],
):

    current_path.append((x, y))

    if x >= x_size or y >= y_size or x < 0 or y < 0:
        return

    current_height = trail_map[y][x]
    if current_height == 9:
        trail_paths.append(current_path)
        return

    # top
    if y > 0 and trail_map[y - 1][x] == current_height + 1:
        traverse_map_part2(
            x, y - 1, x_size, y_size, current_path.copy(), trail_map, trail_paths
        )

    # bottom
    if y < y_size - 1 and trail_map[y + 1][x] == current_height + 1:
        traverse_map_part2(
            x, y + 1, x_size, y_size, current_path.copy(), trail_map, trail_paths
        )

    # left
    if x > 0 and trail_map[y][x - 1] == current_height + 1:
        traverse_map_part2(
            x - 1, y, x_size, y_size, current_path.copy(), trail_map, trail_paths
        )

    # right
    if x < x_size - 1 and trail_map[y][x + 1] == current_height + 1:
        traverse_map_part2(
            x + 1, y, x_size, y_size, current_path.copy(), trail_map, trail_paths
        )


def solve_part1() -> int:
    # input = read_lines("input/day10/example.txt")
    input = read_lines("input/day10/part1.txt")

    trail_map = parse_map(input)
    x_size = len(trail_map[0])
    y_size = len(trail_map)

    total = 0
    for y in range(0, len(trail_map)):
        for x in range(0, len(trail_map[y])):
            if trail_map[y][x] == 0:
                trail_heads = set()
                traverse_map(x, y, x_size, y_size, trail_map, trail_heads)
                # print(f"Trails at ({x},{y}): {trail_heads}")
                total += len(trail_heads)

    return total


def solve_part2() -> int:
    # input = read_lines("input/day10/example.txt")
    input = read_lines("input/day10/part1.txt")

    trail_map = parse_map(input)
    x_size = len(trail_map[0])
    y_size = len(trail_map)

    total = 0
    for y in range(0, len(trail_map)):
        for x in range(0, len(trail_map[y])):

            if trail_map[y][x] == 0:
                trail_paths = []
                traverse_map_part2(x, y, x_size, y_size, [], trail_map, trail_paths)
                # print(f"Trails at ({x},{y}): {len(trail_paths)}")
                # print(trail_paths)
                total += len(trail_paths)

    return total
