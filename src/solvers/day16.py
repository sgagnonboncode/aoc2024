from enum import Enum
from tqdm import tqdm

class Orientation(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class MapPosition(tuple):
    def __new__(cls, x: int, y: int):
        return super().__new__(cls, (x, y))

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]

class Position(tuple):
    def __new__(cls, x: int, y: int, orientation: int = Orientation.NORTH.value):
        return super().__new__(cls, (x, y, orientation))

    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]
    
    @property
    def orientation(self) -> int:
        return self[2]
    


def parse_maze(input_data: str):
    maze = {}
    lines = input_data.strip().splitlines()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            maze[(x, y)] = char
    return maze

def extract_start_and_end(maze)-> tuple[MapPosition, MapPosition]:
    start = None
    goal = None
    for (x, y), char in maze.items():
        if char == 'S':
            start = MapPosition(x, y)
        elif char == 'E':
            goal = MapPosition(x, y)
    if start is None or goal is None:
        raise ValueError("Start or Goal position not found in the maze.")
    return start, goal




# using A* over a 3D drid of (x,y,orientation), find a path from Start to End,
# avoiding walls (#) and moving only in the direction of orientation, with the ability to turn clockwise.
# moving forward costs 1, turning costs 1000.
def heuristic(pos: Position, goal: MapPosition) -> int:
    # manahattan distance, ajusted with minimum turns needed
    dx = abs(pos.x - goal.x)
    dy = abs(pos.y - goal.y)
    min_turns = 0
    if dx !=0 or dy !=0:
        min_turns = 1000
    return dx + dy + min_turns
   
def get_neighbors(maze: dict[tuple[int, int], str], pos: Position) -> list[Position]:
    neighbors = []

    # evaluate moves
    if pos.orientation == Orientation.NORTH.value:
        advance = (pos.x, pos.y - 1)
        side_a = (pos.x -1, pos.y)
        side_b = (pos.x +1, pos.y)
    elif pos.orientation == Orientation.EAST.value:
        advance = (pos.x + 1, pos.y)
        side_a = (pos.x, pos.y -1)
        side_b = (pos.x, pos.y +1)
    elif pos.orientation == Orientation.SOUTH.value:
        advance = (pos.x, pos.y + 1)
        side_a = (pos.x +1, pos.y)
        side_b = (pos.x -1, pos.y)
    elif pos.orientation == Orientation.WEST.value:
        advance = (pos.x - 1, pos.y)
        side_a = (pos.x, pos.y +1)
        side_b = (pos.x, pos.y -1)
    else:
        raise ValueError("Invalid orientation")
    
    if maze.get(advance, '#') != '#':
        neighbors.append(Position(advance[0], advance[1], pos.orientation))
    if maze.get(side_a, '#') != '#':
        neighbors.append(Position(pos.x, pos.y, (pos.orientation -1) % 4))
    if maze.get(side_b, '#') != '#':
        neighbors.append(Position(pos.x, pos.y, (pos.orientation +1) % 4))
        
    return neighbors

def movement_cost(current: Position, neighbor: Position) -> int:
    if (current.x, current.y) != (neighbor.x, neighbor.y):
        return 1  # moving forward
    else:
        return 1000  # turning
    
def reconstruct_path(came_from: dict, current: Position) -> list[Position]:
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def a_star(maze: dict[tuple[int, int], str], start: Position, goal: MapPosition) -> list[Position]:
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

        for neighbor in get_neighbors(maze, current):
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

    return []  # no path found

def evaluate_path(path: list[Position]) -> int:
    total_cost = 0
    for i in range(1, len(path)):
        current = path[i - 1]
        neighbor = path[i]
        if (current.x, current.y) != (neighbor.x, neighbor.y):
            total_cost += 1  # moving forward
        else:
            total_cost += 1000  # turning
    return total_cost

def print_maze_with_path(maze: dict[tuple[int, int], str], path: list[Position]) -> None:
    maze_copy = maze.copy()
    for pos in path:
        maze_copy[(pos.x, pos.y)] = '*'
    max_x = max(x for x, y in maze_copy.keys())
    max_y = max(y for x, y in maze_copy.keys())
    for y in range(max_y + 1):
        line = ''
        for x in range(max_x + 1):
            line += maze_copy.get((x, y), ' ')
        print(line)



def solve_part1() -> int:
    # input_data = open("input/day16/example.txt").read()
    input_data = open("input/day16/part1.txt").read()
    maze = parse_maze(input_data)

    map_start, goal = extract_start_and_end(maze)
    start = Position(map_start.x, map_start.y, Orientation.EAST.value)
    path = a_star(maze, start, goal)

    return evaluate_path(path)

#### Part 2

def find_path_with_midpoint(maze: dict[tuple[int, int], str], start: Position, mid: MapPosition, goal: MapPosition) -> list[Position]:
    # a* , but with a mandatory midpoint
    path_to_mid = a_star(maze, start, mid)
    if not path_to_mid:
        return []
    last_pos = path_to_mid[-1]
    path_to_goal = a_star(maze, last_pos, goal)
    if not path_to_goal:
        return []
    # join the two paths, avoiding double counting the last position of the first path
    combined_path = path_to_mid + path_to_goal[1:]
    return combined_path

def get_open_neighbors(maze: dict[tuple[int, int], str], seatable_pos:set[MapPosition]) -> set[MapPosition]:
    neighbors = set()
    for (x, y), char in maze.items():
        if char not in ('.', 'S', 'E'):
            continue
        pos = MapPosition(x, y)
        if pos in seatable_pos:
            continue

        # check for neighbor in 4 directions
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = MapPosition(x + dx, y + dy)
            if neighbor in seatable_pos:
                neighbors.add(pos)
                break
    return neighbors

def solve_part2() -> int:
    # input_data = open("input/day16/example2.txt").read()
    input_data = open("input/day16/part1.txt").read()
    maze = parse_maze(input_data)
    map_start, goal = extract_start_and_end(maze)
    start = Position(map_start.x, map_start.y, Orientation.EAST.value)

    min_path = a_star(maze, start, goal)
    MINIMUM_COST = evaluate_path(min_path)

    print("Minimum cost from part 1:", MINIMUM_COST)

    # Same as part 1 , but we will try to route trought the neighbors of the current seatable positions
    # using multiple passes, growing the set of seatable positions until no more can be added.

    seatable_positions = set()
    for pos in min_path:
        seatable_positions.add((pos.x, pos.y))
    
    banned_positions = set()

    pass_nb = 0
    while True:
        pass_nb += 1

        neighbors = get_open_neighbors(maze, seatable_positions)
        neighbors = neighbors - banned_positions
        if not neighbors:
            break

        with tqdm(total=len(neighbors), desc=f"Evaluating neighbor, pass#{pass_nb}, seatable:{len(seatable_positions)}, banned:{len(banned_positions)}") as pbar:
            for pos in neighbors:
                path = find_path_with_midpoint(maze, start, pos, goal)
                if path:
                    total_cost = evaluate_path(path)
                    if total_cost == MINIMUM_COST:
                        # add all position in the new path to seatable positions
                        seatable_positions = seatable_positions.union(MapPosition(p.x, p.y) for p in path)
                    else:
                        banned_positions.add(pos)
                else:
                    banned_positions.add(pos)
                pbar.update(1)

    return len(seatable_positions)