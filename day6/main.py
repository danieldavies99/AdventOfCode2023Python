from dataclasses import dataclass
# So easy compared to day 5

@dataclass
class Race:
    time: int
    record_distance: int

def get_numbers_from_line(line: str) -> list[int]:
    parts = line.split(" ")
    res: list[int] = []
    for part in parts:
        if part.isnumeric():
            res.append(int(part))
    return res

def decode_input_part_one(input: str) -> list[Race]:
    parts = input.split('\n')
    times = get_numbers_from_line(parts[0])
    distances = get_numbers_from_line(parts[1])
    res: list[Race] = []
    for i, time in enumerate(times):
        res.append(Race(time, distances[i]))
    return res


def decode_input_part_two(input: str) -> Race:
    parts = input.split('\n')
    times = get_numbers_from_line(parts[0])
    distances = get_numbers_from_line(parts[1])
    stitched_time = ""
    stitched_distance = ""
    for i, time in enumerate(times):
        stitched_time += str(time)
        stitched_distance += str(distances[i])
    return Race(int(stitched_time), int(stitched_distance))

def calc_distance_from_time_held(time_held: int, race_time: int) -> int:
    return time_held * (race_time - time_held)

def get_num_wins(race: Race) -> int:
    i = 0
    start = -1
    end = -1
    while i < race.time / 2:
        if start == -1:
            dist1 = calc_distance_from_time_held(i, race.time)
            if dist1 > race.record_distance:
                start = i
        
        if end == -1:
            dist2 = calc_distance_from_time_held(race.time - i, race.time)
            if dist2 > race.record_distance:
                end = race.time - i
        i += 1
    return end - start + 1


def solve_part_one(input: str) -> int:
    races: list[Race] = decode_input_part_one(input)
    ways_to_win: list[int] = []
    for race in races:
        ways_to_win.append(get_num_wins(race))
    print("num ways to win {}".format(ways_to_win))
    res = 0
    for way_to_win in ways_to_win:
        if res == 0:
            res = way_to_win
            continue
        res *= way_to_win
    return res

def solve_part_two(input: str) -> int:
    race: Race = decode_input_part_two(input)
    ways_to_win = get_num_wins(race)
    return ways_to_win

input = open("example_input.txt").read()

print("Part one: {}".format(solve_part_one(input)))
print("Part two: {}".format(solve_part_two(input)))
