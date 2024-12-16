from src.solvers.day15 import big_robot_step2, expand_map, parse_input, print_bigger_map
from src.common.file_utils import read_lines


puzzle_input = read_lines("input/day15/example.txt")
# input = read_lines("input/day15/part1.txt")

warehouse_map, robot_instructions, position = parse_input(puzzle_input)
bigger_map, position = expand_map(warehouse_map, position)

print_bigger_map(bigger_map)

print(f"Position: {position}")

step = 0
while True:

    # read arrow key
    key = input("Press arrow key (w, a, s, d) to move robot. Press q to quit: ")
    if key == "q":
        break

    instruction = "z"

    if key == "w":
        instruction = "^"
    elif key == "s":
        instruction = "v"
    elif key == "a":
        instruction = "<"
    elif key == "d":
        instruction = ">"
    else:
        print("Invalid key")
        continue

    step += 1

    previous_position = position

    print(f"Step: {step} - Instruction: {instruction}")
    position = big_robot_step2(bigger_map, position, instruction)

    if previous_position == position:
        print(f"ROBOT IS STUCK AT {position}")

    print_bigger_map(bigger_map)


print("Final position: ", position)
print_bigger_map(bigger_map)
