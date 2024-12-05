from typing import Tuple
from src.common.file_utils import read_lines
import re


def parse_xmas_grid(lines: list[str]) -> list[list[chr]]:
    grid: list[list[chr]] = []

    for line in lines:
        grid.append([c for c in line if c != "\n"])

    return grid


def reduce_grid(grid: list[list[chr]]) -> int:

    grid_width = len(grid[0])
    grid_height = len(grid)

    # match_grid:list[list[int]] = [[0 for i in range(grid_width)] for j in range(grid_height)]
    hits = 0

    # XMAS  <=> SAMX
    for i in range(0, grid_height):
        for j in range(0, grid_width - 3):

            if (
                grid[i][j] == "X"
                and grid[i][j + 1] == "M"
                and grid[i][j + 2] == "A"
                and grid[i][j + 3] == "S"
            ):
                # match_grid[i][j] += 1
                # match_grid[i][j+1] += 1
                # match_grid[i][j+2] += 1
                # match_grid[i][j+3] += 1
                hits = hits + 1

            elif (
                grid[i][j] == "S"
                and grid[i][j + 1] == "A"
                and grid[i][j + 2] == "M"
                and grid[i][j + 3] == "X"
            ):
                # match_grid[i][j] += 1
                # match_grid[i][j+1] += 1
                # match_grid[i][j+2] += 1
                # match_grid[i][j+3] += 1
                hits = hits + 1

    # X        S
    #  M   <=>  A
    #   A        M
    #    S        X
    for i in range(0, grid_height - 3):
        for j in range(0, grid_width - 3):

            if (
                grid[i][j] == "X"
                and grid[i + 1][j + 1] == "M"
                and grid[i + 2][j + 2] == "A"
                and grid[i + 3][j + 3] == "S"
            ):
                # match_grid[i][j] += 1
                # match_grid[i+1][j+1] += 1
                # match_grid[i+2][j+2] += 1
                # match_grid[i+3][j+3] += 1
                hits = hits + 1

            elif (
                grid[i][j] == "S"
                and grid[i + 1][j + 1] == "A"
                and grid[i + 2][j + 2] == "M"
                and grid[i + 3][j + 3] == "X"
            ):
                # match_grid[i][j] += 1
                # match_grid[i+1][j+1] += 1
                # match_grid[i+2][j+2] += 1
                # match_grid[i+3][j+3] += 1
                hits = hits + 1

    # X     S
    # M  <=>A
    # A     M
    # S     X
    for i in range(0, grid_height - 3):
        for j in range(0, grid_width):

            if (
                grid[i][j] == "X"
                and grid[i + 1][j] == "M"
                and grid[i + 2][j] == "A"
                and grid[i + 3][j] == "S"
            ):
                # match_grid[i][j] += 1
                # match_grid[i+1][j] += 1
                # match_grid[i+2][j] += 1
                # match_grid[i+3][j] += 1
                hits = hits + 1

            elif (
                grid[i][j] == "S"
                and grid[i + 1][j] == "A"
                and grid[i + 2][j] == "M"
                and grid[i + 3][j] == "X"
            ):
                # match_grid[i][j] += 1
                # match_grid[i+1][j] += 1
                # match_grid[i+2][j] += 1
                # match_grid[i+3][j] += 1
                hits = hits + 1

    #    S         X
    #   A         M
    #  M   <=>   A
    # X         S
    for i in range(0, grid_height - 3):
        for j in range(0, grid_width - 3):

            if (
                grid[i + 3][j] == "X"
                and grid[i + 2][j + 1] == "M"
                and grid[i + 1][j + 2] == "A"
                and grid[i][j + 3] == "S"
            ):
                # match_grid[i+3][j] += 1
                # match_grid[i+2][j+1] += 1
                # match_grid[i+1][j+2] += 1
                # match_grid[i][j+3] += 1
                hits = hits + 1

            elif (
                grid[i + 3][j] == "S"
                and grid[i + 2][j + 1] == "A"
                and grid[i + 1][j + 2] == "M"
                and grid[i][j + 3] == "X"
            ):
                # match_grid[i+3][j] += 1
                # match_grid[i+2][j+1] += 1
                # match_grid[i+1][j+2] += 1
                # match_grid[i][j+3] += 1
                hits = hits + 1

    # print("Match Grid")
    # for row in match_grid:
    #     print(row)

    return hits


def reduce_grid2(grid: list[list[chr]]) -> int:

    grid_width = len(grid[0])
    grid_height = len(grid)

    # match_grid:list[list[int]] = [[0 for i in range(grid_width)] for j in range(grid_height)]
    hits = 0

    # search only for cross MAS match
    #  ex:  M S
    #        A
    #       M S
    for i in range(1, grid_height - 1):
        for j in range(1, grid_width - 1):
            if grid[i][j] != "A":
                continue

            if grid[i - 1][j - 1] not in ["M", "S"]:
                continue

            if grid[i + 1][j + 1] not in ["M", "S"]:
                continue

            if grid[i - 1][j + 1] not in ["M", "S"]:
                continue

            if grid[i + 1][j - 1] not in ["M", "S"]:
                continue

            if grid[i - 1][j - 1] == grid[i + 1][j + 1]:
                continue

            if grid[i - 1][j + 1] == grid[i + 1][j - 1]:
                continue

            # match_grid[i-1][j-1] += 1
            # match_grid[i+1][j+1] += 1
            # match_grid[i][j] += 1
            # match_grid[i-1][j+1] += 1
            # match_grid[i+1][j-1] += 1
            hits = hits + 1

    # print("Match Grid")
    # for row in match_grid:
    #     print(row)

    return hits


def solve_part1() -> int:
    # lines = read_lines("input/day04/example.txt")
    lines = read_lines("input/day04/part1.txt")
    grid = parse_xmas_grid(lines)

    # for row in grid:
    #     print(row)

    hits = reduce_grid(grid)

    return hits


def solve_part2() -> int:
    # lines = read_lines("input/day04/example.txt")
    lines = read_lines("input/day04/part1.txt")
    grid = parse_xmas_grid(lines)

    # for row in grid:
    #     print(row)

    hits = reduce_grid2(grid)

    return hits
