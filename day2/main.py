from dataclasses import dataclass

lines = open("input.txt").read().split("\n")

# define number of cubes in bag
RED_LIMIT: int = 12
GREEN_LIMIT: int = 13
BLUE_LIMIT: int = 14

@dataclass
class CubeSet:
    red: int
    green: int
    blue: int

class Game:
    id: int
    sets: list[CubeSet]

def decode_game(line: str) -> Game:

    res = Game()

    # get game index
    index_str: str = line.split(":")[0][5:]
    print(index_str)
    index_int = int(index_str)
    res.id = index_int

    set_strs = line.split(":")[1].split(";")
    # input looks like " 4 red, 5 blue, 9 green"
    def decode_set(set: str) -> CubeSet:
        set = set[1:] # remove preceeding space
        cube_counts = set.split(", ")
        res = CubeSet(0,0,0)
        for cube_count in cube_counts:
            parts = cube_count.split(" ")
            num = int(parts[0])
            color = parts[1]
            if color == "red":
                res.red += num
            if color == "green":
                res.green += num
            if color == "blue":
                res.blue += num
        return res

    # decode sets
    sets: list[CubeSet] = []
    for set_str in set_strs:
        sets.append(decode_set(set_str))    
    res.sets = sets

    return res

# game1 = decode_game(lines[0])

def decode_all_games(lines: list[str]) -> list[Game]:
    res: list[Game] = []
    for line in lines:
        res.append(decode_game(line))
    return res

def get_only_possible_games(
        games: list[Game],
        total_num_red: int,
        total_num_green: int,
        total_num_blue: int
    ) -> list[Game]:
    res: list[Game] = []
    for game in games:
        is_possible = True
        for set in game.sets:
            if set.red > total_num_red or set.green > total_num_green or set.blue > total_num_blue:
                is_possible = False
        if is_possible:
            res.append(game)
    return res
    
def sum_ids(games: list[Game]) -> int:
    sum = 0
    for game in games:
        sum += game.id
    return sum

games: list[Game] = decode_all_games(lines)
possible_games: list[Game] = get_only_possible_games(games, RED_LIMIT, GREEN_LIMIT, BLUE_LIMIT)
res = sum_ids(possible_games)
print("solution 1 {}".format(res))