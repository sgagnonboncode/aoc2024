from pydantic import BaseModel
from src.common.file_utils import read_lines
from tqdm import tqdm

class MapPosition(tuple[int, int]):
    
    @property
    def x(self) -> int:
        return self[0]
    
    @property
    def y(self) -> int:
        return self[1]
    
    def manhattan_distance(self, other: "MapPosition") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

class Racetrack():
    def __init__(self, positions: list[MapPosition], walls: set[MapPosition]):
        self.positions = positions
        self.walls = walls
        self.start = positions[0]
        self.end = positions[-1]
        # 'value' of each position = its index in the racetrack, Start =0, End = len-1
        self.race_values = {pos: idx for idx, pos in enumerate(positions)}

def parse_racetrack(lines: list[str]) -> Racetrack:
    racetrack: list[MapPosition] = []

    start:MapPosition|None = None
    end:MapPosition|None = None
    unordered_positions:set[MapPosition] = set()
    walls:set[MapPosition] = set()

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start = MapPosition((x, y))
            elif char == "E":
                end = MapPosition((x, y))
            elif char ==".":
                unordered_positions.add(MapPosition((x, y)))
            elif char =="#":
                walls.add(MapPosition((x, y)))

    if start is None or end is None:
        raise ValueError("Racetrack must have a start and end position.")

    racetrack.append(start)

    adjacent_offsets = [(-1,0),(1,0),(0,-1),(0,1)]
    with tqdm(total=len(unordered_positions), desc="Ordering racetrack") as pbar:
        while len(unordered_positions) >0:
            # dont bother pathfinding, just pop adjacent positions
            # since we already know the racetrack is continuous
            current = racetrack[-1]

            for offset in adjacent_offsets:
                adjacent = MapPosition((current.x+offset[0], current.y+offset[1]))
                if adjacent in unordered_positions:
                    racetrack.append(adjacent)
                    unordered_positions.remove(adjacent)
                    break
            pbar.update(1)

    racetrack.append(end)

    return Racetrack(positions=racetrack, walls=walls)
   


class Cheat():

    def __init__(self, initial: MapPosition, end: MapPosition, cheat_value: int):
        self.initial: MapPosition = initial
        self.end:MapPosition = end
        self.cheat_value: int = cheat_value

def part_1_cheats(race_track: Racetrack) -> list[Cheat]:
    # at each step , scan for possible shortcuts.
    # no actual pathfinding is needed for this, we only care
    # for how many steps we can save
    adjacent = [(-1,0),(1,0),(0,-1),(0,1)]

    cheats:list[Cheat] = []

    with tqdm(total=len(race_track.positions), desc="Scanning for cheats") as pbar:
        for pos in race_track.positions:
            pbar.set_postfix({"Current Position": f"{pos}"})

            # look for walls adjacent to current position
            for ajd_offset in adjacent:
                ajd = MapPosition((pos.x+ajd_offset[0], pos.y+ajd_offset[1]))
                if ajd in race_track.positions:
                    # not a wall, skip
                    continue

                # look for possible re-entries from this wall position
                for re_entry_offset in adjacent:
                    re_entry = MapPosition((ajd.x+re_entry_offset[0], ajd.y+re_entry_offset[1]))
                    if re_entry not in race_track.positions:
                        # not a valid re-entry, skip
                        continue

                    # valid re-entry found, calculate cheat value
                    cheat_value = race_track.race_values[re_entry] - race_track.race_values[pos] -2

                    if cheat_value <= 0:
                        # not an actual cheat, skip
                        continue

                    cheats.append(Cheat(
                        initial=pos,
                        end=re_entry,
                        cheat_value=cheat_value
                    ))
            pbar.update(1)
    return cheats

def solve_part1() -> int:
    # input_lines = read_lines("input/day20/example.txt")
    input_lines = read_lines("input/day20/part1.txt")

    race_track = parse_racetrack(input_lines)
    cheats = part_1_cheats(race_track)

    cheat_grouped_by_value:dict[int, int] = {}
    for cheat in cheats:
        cheat_grouped_by_value.setdefault(cheat.cheat_value, 0)
        cheat_grouped_by_value[cheat.cheat_value] +=1

    part1= 0
    for value, count in cheat_grouped_by_value.items():
        if value >= 100:
            part1+=count
    return part1

def solve_part2() -> int:
    # input_lines = read_lines("input/day20/example.txt")
    # MIN_CHEAT_VALUE = 50

    input_lines = read_lines("input/day20/part1.txt")
    MIN_CHEAT_VALUE = 100
    MAX_CHEAT_DURATION = 20
    race_track = parse_racetrack(input_lines)

    part_2 = 0
    # all_cheats:dict[int,int] = {} 

    # completely ignore the walls this time, just look for possible shortcuts within the distance
    with tqdm(total=len(race_track.positions), desc="Scanning for cheats") as pbar:
        for cur in range(len(race_track.positions)):

            # pointless to scan for cheats under the threshold, only look ahead the track
            for look_ahead in range(cur+MIN_CHEAT_VALUE, len(race_track.positions)):
                # check if we can reach it withing the max cheat duration using
                #  the manathan distance between that wall and the lookahead position
                dist = race_track.positions[cur].manhattan_distance(race_track.positions[look_ahead])
                if dist <= MAX_CHEAT_DURATION: 
                    # by definition , max cheat duration is <<<< to the min cheat value,
                    # check the cheat value again , ajusted for the distance to see if the 
                    # cheat is still considered good
                    cheat_value = look_ahead - cur - dist
                    if cheat_value >= MIN_CHEAT_VALUE:
                        # valid cheat found
                        # all_cheats.setdefault(cheat_value, 0)
                        # all_cheats[cheat_value] +=1
                        part_2 +=1
            pbar.update(1)

    # for value, count in sorted(all_cheats.items()):
        # print(f"There are {count} cheats that save {value} picoseconds.")

    return part_2

    