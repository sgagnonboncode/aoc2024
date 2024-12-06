from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel


def load_floor_plan(lines: list[str]) -> list[list[str]]:
    floor_plan = []

    for line in lines:
        if len(line) == 0:
            continue

        floor_plan.append([c for c in line[:-1]])

    return floor_plan


def find_starting_position(floor_plan: list[list[str]]) -> Tuple[int, int]:
    for y in range(len(floor_plan)):
        for x in range(len(floor_plan[y])):
            if floor_plan[y][x] == "^":
                return (x, y)

    raise ValueError("No starting position found")


class GuardState(BaseModel):
    x: int
    y: int
    # 0 = up, 1 = right, 2 = down, 3 = left
    orientation: int

    def turn_right(self):
        self.orientation = (self.orientation + 1) % 4

    def ahead(self) -> Tuple[int, int]:
        if self.orientation == 0:
            return (self.x, self.y - 1)
        elif self.orientation == 1:
            return (self.x + 1, self.y)
        elif self.orientation == 2:
            return (self.x, self.y + 1)
        elif self.orientation == 3:
            return (self.x - 1, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.orientation))


class GuardSimulationPart1:

    def __init__(self, floor_plan: list[list[str]], guard: GuardState):
        self.floor_plan = floor_plan
        self.guard = guard

        self.max_x = len(floor_plan[0])
        self.max_y = len(floor_plan)

        self.visited = [[0] * self.max_x for i in range(self.max_y)]
        self.visited[guard.y][guard.x] = 1

    def simulate_one_step(self) -> bool:
        next_x, next_y = self.guard.ahead()

        if not (self.max_x > next_x >= 0 and self.max_y > next_y >= 0):
            # exiting the map

            return False

        if self.floor_plan[next_y][next_x] == "#":
            # obstacle ahead : turn right without moving
            self.guard.orientation = (self.guard.orientation + 1) % 4
            return True

        # move forward
        self.guard.x = next_x
        self.guard.y = next_y

        # mark as visited and keep moving
        self.visited[next_y][next_x] += 1

        return True

    def simulate(self) -> int:
        while self.simulate_one_step():
            pass

        total = 0
        for row in self.visited:
            for cell in row:
                if cell > 0:
                    total += 1

        return total


class GuardSimulationPart2:

    def __init__(self, floor_plan: list[list[str]], guard: GuardState):
        self.floor_plan = floor_plan
        self.guard = guard
        self.max_x = len(floor_plan[0])
        self.max_y = len(floor_plan)

    def simulate(self) -> int:
        original_position = (self.guard.x, self.guard.y)
        guard = GuardState(
            x=self.guard.x, y=self.guard.y, orientation=self.guard.orientation
        )

        looping_obstacle_locations: set[Tuple[int, int]] = set()
        while True:

            next_x, next_y = guard.ahead()
            if not (self.max_x > next_x >= 0 and self.max_y > next_y >= 0):
                # exiting the map
                break

            if self.floor_plan[next_y][next_x] == "#":
                # obstacle ahead : turn right without moving
                guard.turn_right()
                continue

            # test if placing an obstacle here will cause a loop
            if ((next_x, next_y) not in looping_obstacle_locations) and (
                next_x,
                next_y,
            ) != original_position:

                visited_loop: set[GuardState] = set()
                guard_loop = GuardState(
                    x=self.guard.x, y=self.guard.y, orientation=self.guard.orientation
                )
                visited_loop.add(
                    GuardState(
                        x=guard_loop.x,
                        y=guard_loop.y,
                        orientation=guard_loop.orientation,
                    )
                )

                while True:
                    loop_x, loop_y = guard_loop.ahead()

                    if not (self.max_x > loop_x >= 0 and self.max_y > loop_y >= 0):
                        # exiting the map : no loop
                        break

                    if (loop_x, loop_y) == (next_x, next_y) or self.floor_plan[loop_y][
                        loop_x
                    ] == "#":
                        # obstacle ahead : turn right without moving
                        guard_loop.turn_right()
                        continue

                    # keep moving
                    guard_loop.x = loop_x
                    guard_loop.y = loop_y

                    if guard_loop in visited_loop:
                        # loop detected
                        looping_obstacle_locations.add((next_x, next_y))
                        # print(f"Looping obstacle at {next_x},{next_y} detected, loop length = {len(visited_loop)}")
                        break

                    visited_loop.add(
                        GuardState(
                            x=guard_loop.x,
                            y=guard_loop.y,
                            orientation=guard_loop.orientation,
                        )
                    )

            # move forward along the original path
            guard.x = next_x
            guard.y = next_y

        return len(looping_obstacle_locations)


def solve_part1() -> int:
    # lines = read_lines("input/day06/example.txt")
    lines = read_lines("input/day06/part1.txt")
    floor_plan = load_floor_plan(lines)

    start_x, start_y = find_starting_position(floor_plan)

    guard = GuardState(x=start_x, y=start_y, orientation=0)
    simulation = GuardSimulationPart1(floor_plan, guard)

    return simulation.simulate()


def solve_part2() -> int:
    # lines = read_lines("input/day06/example.txt")
    lines = read_lines("input/day06/part1.txt")

    floor_plan = load_floor_plan(lines)
    start_x, start_y = find_starting_position(floor_plan)

    guard = GuardState(x=start_x, y=start_y, orientation=0)
    simulation = GuardSimulationPart2(floor_plan, guard)

    return simulation.simulate()
