from enum import Enum
from functools import cache
from itertools import repeat
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


def parse_input(input: list[str]) -> list[list[chr]]:
    return [list(line[:-1]) for line in input]


class NodePosition(BaseModel):
    x: int
    y: int


class Region(BaseModel):
    node_type: str
    x0: int
    y0: int
    nodes: list[NodePosition] = []

    def get_perimeter(self):
        x_min = min([n.x for n in self.nodes])
        x_max = max([n.x for n in self.nodes])
        y_min = min([n.y for n in self.nodes])
        y_max = max([n.y for n in self.nodes])

        fences = 0

        nodes = set([(n.x, n.y) for n in self.nodes])

        for node in nodes:
            if node[0] > x_min and (node[0] - 1, node[1]) not in nodes:
                fences += 1
            elif node[0] == x_min:
                fences += 1

            if node[0] < x_max and (node[0] + 1, node[1]) not in nodes:
                fences += 1
            elif node[0] == x_max:
                fences += 1

            if node[1] > y_min and (node[0], node[1] - 1) not in nodes:
                fences += 1
            elif node[1] == y_min:
                fences += 1

            if node[1] < y_max and (node[0], node[1] + 1) not in nodes:
                fences += 1
            elif node[1] == y_max:
                fences += 1

        # print()
        # for y in range(y_min, y_max + 1):
        #     for x in range(x_min, x_max + 1):
        #         if (x, y) in nodes:
        #             print("#", end="")
        #         else:
        #             print(".", end="")

        #     print()

        return fences

    def get_sides(self):

        x_min = min([n.x for n in self.nodes])
        x_max = max([n.x for n in self.nodes])
        y_min = min([n.y for n in self.nodes])
        y_max = max([n.y for n in self.nodes])

        nodes = set([(n.x, n.y) for n in self.nodes])

        nodes_fence = {}

        # merge fences, checking in the direction away from x_min,y_min
        # first walk the perimeter as per part1 , but then remove fences that are adjacent
        sides = 0
        for node in nodes:

            up = False
            right = False
            down = False
            left = False

            # left side
            if node[0] == x_min or (
                node[0] > x_min and (node[0] - 1, node[1]) not in nodes
            ):
                sides += 1
                left = True

            # right side
            if node[0] == x_max or (
                node[0] < x_max and (node[0] + 1, node[1]) not in nodes
            ):
                sides += 1
                right = True

            # top side
            if node[1] == y_min or (
                node[1] > y_min and (node[0], node[1] - 1) not in nodes
            ):
                sides += 1
                up = True

            # bottom side
            if node[1] == y_max or (
                node[1] < y_max and (node[0], node[1] + 1) not in nodes
            ):
                sides += 1
                down = True

            nodes_fence[node] = (up, right, down, left)

        # adjacent fences, check away from x_min,y_min
        for node in nodes:

            if (node[0], node[1] + 1) in nodes:

                if nodes_fence[node][1] and nodes_fence[(node[0], node[1] + 1)][1]:
                    sides -= 1

                if nodes_fence[node][3] and nodes_fence[(node[0], node[1] + 1)][3]:
                    sides -= 1

            if (node[0] + 1, node[1]) in nodes:

                if nodes_fence[node][0] and nodes_fence[(node[0] + 1, node[1])][0]:
                    sides -= 1

                if nodes_fence[node][2] and nodes_fence[(node[0] + 1, node[1])][2]:
                    sides -= 1

        return sides

    def get_area(self):
        return len(self.nodes)


def scan_regions(garden_map: list[list[chr]]) -> list[Region]:

    map_height = len(garden_map)
    map_width = len(garden_map[0])

    regions = []

    solved = [[False for x in range(map_width)] for y in range(map_height)]

    for y in range(map_height):
        for x in range(map_width):

            if solved[y][x]:
                continue

            c = garden_map[y][x]
            current_region: set[Tuple[int, int]] = set()
            explore_region(x, y, map_width, map_height, garden_map, c, current_region)

            nodes = [NodePosition(x=t[0], y=t[1]) for t in current_region]
            region = Region(node_type=str(c), x0=x, y0=y, nodes=nodes)
            regions.append(region)

            for node in current_region:
                solved[node[1]][node[0]] = True

    return regions


def explore_region(
    x: int,
    y: int,
    x_len: int,
    y_len: int,
    garden_map: list[list[chr]],
    c: chr,
    adjacent_nodes: set[Tuple[int, int]],
):

    if x < 0 or y < 0 or x >= x_len or y >= y_len:
        return

    if garden_map[y][x] != c:
        return

    if (x, y) in adjacent_nodes:
        return

    adjacent_nodes.add((x, y))

    explore_region(x - 1, y, x_len, y_len, garden_map, c, adjacent_nodes)
    explore_region(x + 1, y, x_len, y_len, garden_map, c, adjacent_nodes)
    explore_region(x, y - 1, x_len, y_len, garden_map, c, adjacent_nodes)
    explore_region(x, y + 1, x_len, y_len, garden_map, c, adjacent_nodes)


def solve_part1() -> int:
    # input = read_lines("input/day12/example.txt")
    input = read_lines("input/day12/part1.txt")

    garden_map = parse_input(input)
    regions = scan_regions(garden_map)

    price = 0
    for region in regions:
        # print(f"Region {region.node_type} at {region.x0},{region.y0} Area: {region.get_area()} Perimeter: {region.get_perimeter()}")
        price += region.get_area() * region.get_perimeter()

    return price


def solve_part2() -> int:
    # input = read_lines("input/day12/example.txt")
    input = read_lines("input/day12/part1.txt")

    garden_map = parse_input(input)
    regions = scan_regions(garden_map)

    price = 0
    for region in regions:
        # print(f"Region {region.node_type} at {region.x0},{region.y0} Area: {region.get_area()} Perimeter:{region.get_perimeter()} Sides: {region.get_sides()}")
        price += region.get_area() * region.get_sides()

    return price
