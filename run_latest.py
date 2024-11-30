import sys
from glob import glob
from importlib import import_module

from colorama import Fore, Back, Style


# display the current solver with some fancy x-mas colors
def display_splash_title():
    banner = [
        Fore.YELLOW + "         |",
        Fore.YELLOW + "        -+-",
        Fore.YELLOW + "         A",
        Fore.GREEN + "        /=\\            ",
        Fore.GREEN
        + "      "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " \\"
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "          ",
        Fore.GREEN + "      /=====\\          ",
        Fore.GREEN
        + "      /  "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "  \\         "
        + Fore.RED
        + "      _    ___   ____   ____   ___ ____  _  _  ",
        Fore.GREEN
        + "    "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " * "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " \\"
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "       "
        + Fore.RED
        + "     / \\  / _ \\ / ___| |___ \\ / _ \\___ \\| || |  ",
        Fore.GREEN
        + "    /=========\\       "
        + Fore.RED
        + "    / _ \\| | | | |       __) | | | |__) | || |_ ",
        Fore.GREEN
        + "    /  *   *  \\       "
        + Fore.RED
        + "   / ___ \\ |_| | |___   / __/| |_| / __/|__   _|",
        Fore.GREEN
        + "  "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + " \\"
        + Fore.WHITEO
        + "i"
        + Fore.GREEN
        + "     "
        + Fore.RED
        + "  /_/   \\_\\___/ \\____| |_____|\\___/_____|  |_|  ",
        Fore.GREEN + "  /=============\\      ",
        Fore.GREEN
        + "  /  "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   "
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "  \\      ",
        Fore.GREEN
        + Fore.WHITE
        + "i"
        + Fore.GREEN
        + "/ *   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   "
        + Fore.RED
        + "O"
        + Fore.GREEN
        + "   * \\"
        + Fore.WHITE
        + "i"
        + Fore.GREEN,
        Fore.GREEN + "/=================\\",
        Fore.BLACK + "       |___|",
    ]

    for banner_line in banner:
        print(Fore.RED + banner_line + Fore.RESET)

    solving = list("Solving")
    colors = [Fore.GREEN, Fore.WHITE, Fore.RED]
    cidx = 0
    for c in solving:
        print(colors[cidx % len(colors)], c, Fore.RESET, sep="", end="", flush=False)
        cidx = cidx + 1


display_splash_title()


# import the latest solver and run it
solvers = sorted(glob("./src/solvers/day*.py"))
latest = solvers[-1]
solver_name = latest.split("/")[-1][:-3]

print(Fore.RESET, solver_name, "...")
solver = import_module(f"src.solvers.{ solver_name}")

print(Fore.CYAN + "Part 1" + Fore.RESET + ":", solver.solve_part1())
print(Fore.CYAN + "Part 2" + Fore.RESET + ":", solver.solve_part2())
