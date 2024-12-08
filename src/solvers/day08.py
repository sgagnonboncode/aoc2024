from enum import Enum
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


def parse_antinode_map(lines: list[str]) -> list[list[chr]]:
    antinode_map = []
    for line in lines:
        nodes = [c for c in line[:-1]]
        if len(nodes) == 0:
            continue

        antinode_map.append(nodes)
    return antinode_map


def compute_signal(
    antinode_map: list[list[chr]], consider_harmonics: bool = False
) -> dict[chr, set]:

    max_x = len(antinode_map[0])
    max_y = len(antinode_map)

    signals_maps: dict[chr, set] = {}
    node_positions: dict[chr, list[tuple[int, int]]] = {}

    for y in range(max_y):
        for x in range(max_x):

            if antinode_map[y][x] == ".":
                continue

            node_type = antinode_map[y][x]
            node_pos = (x, y)

            node_positions.setdefault(node_type, [])
            node_positions[node_type].append(node_pos)

            signals_maps.setdefault(node_type, set())

            if consider_harmonics:
                signals_maps[node_type].add(node_pos)

    for node_type in node_positions:
        for i in range(len(node_positions[node_type])):
            for j in range(len(node_positions[node_type])):
                if i == j:
                    continue

                x1, y1 = node_positions[node_type][i]
                x2, y2 = node_positions[node_type][j]

                dist_x = x2 - x1
                dist_y = y2 - y1

                harmonic_index = 1
                while True:

                    echo_x = x1 - (dist_x * harmonic_index)
                    echo_y = y1 - (dist_y * harmonic_index)

                    if not (0 <= echo_x < max_x and 0 <= echo_y < max_y):
                        break

                    if antinode_map[echo_y][echo_x] == node_type:
                        continue

                    signals_maps[node_type].add((echo_x, echo_y))

                    if not consider_harmonics:
                        break

                    harmonic_index += 1

    return signals_maps


def solve_part1() -> int:
    # lines = read_lines("input/day08/example.txt")
    lines = read_lines("input/day08/part1.txt")

    antinode_map = parse_antinode_map(lines)
    signals_maps = compute_signal(antinode_map)

    unique_positions = set()
    for node_type in signals_maps:
        echos = signals_maps[node_type]
        unique_positions.update(echos)

    return len(unique_positions)


def solve_part2() -> int:
    # lines = read_lines("input/day08/example.txt")
    lines = read_lines("input/day08/part1.txt")

    antinode_map = parse_antinode_map(lines)
    signals_maps = compute_signal(antinode_map, consider_harmonics=True)

    unique_positions = set()
    for node_type in signals_maps:
        echos = signals_maps[node_type]
        unique_positions.update(echos)

    return len(unique_positions)
