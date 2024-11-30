import sys
from glob import glob
from importlib import import_module

solvers = sorted(glob("./src/solvers/day*.py"))
latest = solvers[-1]

solver_name = latest.split("/")[-1][:-3]
print("Solving", solver_name, "...")
solver = import_module(f"src.solvers.{ solver_name}")

print("Part 1:", solver.solve_part1())
print("Part 2:", solver.solve_part2())