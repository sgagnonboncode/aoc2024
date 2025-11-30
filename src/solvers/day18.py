from src.common.file_utils import read_lines


def build_grid(input_lines:list[str]) -> dict[tuple[int,int],int]:
    
    maze = {}
    timer = 1
    for line in input_lines:
        x_str, y_str = line.split(",")
        x = int(x_str.strip())
        y = int(y_str.strip())
        maze[(x, y)] = timer
        timer += 1

    return maze

INT_MAX = 2**31 -1

def print_grid(grid:dict[tuple[int,int],int],elapsed_time:int=0, path:list[MapPosition]=[])->None:
    max_x = max(x for x, y in grid.keys())
    max_y = max(y for x, y in grid.keys())
    path_set = set(path)
    for y in range(max_y + 1):
        row_str = ""
        for x in range(max_x + 1):
            if (x, y) in path_set:
                row_str += "O"
                continue
            val = grid.get((x, y), INT_MAX)
            if val > elapsed_time:
                row_str += "."
            else:
                row_str += "#"
        print(row_str)



class MapPosition(tuple):
    def __new__(cls, x: int, y: int):
        return super().__new__(cls, (x, y))

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]

def heuristic(pos: MapPosition, goal: MapPosition) -> int:
    # manahattan distance
    dx = abs(pos.x - goal.x)
    dy = abs(pos.y - goal.y)
    return dx + dy
   
def get_neighbors(maze: dict[tuple[int, int], int], pos: MapPosition, move_count:int=0) -> list[MapPosition]:
    neighbors = []

    # check four sides
    deltas = [(-1,0),(1,0),(0,-1),(0,1)]

    # check if the position is currently open
    for dx, dy in deltas:
        new_x = pos.x + dx
        new_y = pos.y + dy
        if (new_x, new_y) in maze:
            if move_count < maze[(new_x, new_y)]:
                neighbors.append(MapPosition(new_x, new_y))
        elif new_x >=0 and new_y >=0 and new_x <= max(x for x,y in maze.keys()) and new_y <= max(y for x,y in maze.keys()):
            neighbors.append(MapPosition(new_x, new_y))
        
    return neighbors

def movement_cost(current: MapPosition, neighbor: MapPosition) -> int:
    return 1
    
def reconstruct_path(came_from: dict, current: MapPosition) -> list[MapPosition]:
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def a_star(maze: dict[tuple[int, int], int], start: MapPosition, goal: MapPosition, time:int) -> list[MapPosition]:
    closed_set = set()
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        current = min(open_set, key=lambda pos: f_score.get(pos, float('inf')))
        if (current.x, current.y) == (goal.x, goal.y):
            return reconstruct_path(came_from, current)
        
        open_set.remove(current)
        closed_set.add(current)

        for neighbor in get_neighbors(maze, current, time):
            if neighbor in closed_set:
                continue
            
            tentative_g_score = g_score[current] + movement_cost(current, neighbor)

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

    print("No path found")
    return []  # no path found


def solve_part1() -> int:
    # input_lines = read_lines("input/day18/example.txt")
    # goal_pos = MapPosition(6,6)

    input_lines = read_lines("input/day18/part1.txt")
    goal_pos = MapPosition(70,70)


    grid = build_grid(input_lines)
    start_pos = MapPosition(0,0)

    TIMER = 1024
    
    path = a_star(grid, start_pos, goal_pos, time=TIMER)
    # print_grid(grid, elapsed_time=TIMER, path=path)

    return len(path)-1

def solve_part2() -> str:

    # input_lines = read_lines("input/day18/example.txt")
    # goal_pos = MapPosition(6,6)
    # TIMER = 12
    input_lines = read_lines("input/day18/part1.txt")
    goal_pos = MapPosition(70,70)
    TIMER = 1024
    
    maze = build_grid(input_lines)
    start_pos = MapPosition(0,0)
    
    path = a_star(maze, start_pos, goal_pos, time=TIMER)
    print_grid(maze, elapsed_time=TIMER, path=path)

    falling_blocks = sorted([MapPosition(pos[0], pos[1]) for pos in maze], key=lambda p: maze[p])

    for pos in falling_blocks:
        if pos not in path:
            # dont care about positions not in CURRENT path
            continue

        if maze[(pos.x, pos.y)] > TIMER:
            print(f"Position {pos} is blocked at time {maze[(pos.x, pos.y)]} within TIMER {TIMER}")
            # recompute the path
            alternate_time = maze[(pos.x, pos.y)]
            path = a_star(maze, start_pos, goal_pos, time=alternate_time)
            print_grid(maze, elapsed_time=alternate_time, path=path)
            if path:
                print(f"Alternate path found at time {alternate_time}:")
            else:
                print(f"No alternate path found at time {alternate_time}")
                return f"{pos.x},{pos.y}"

    return "-1"
    