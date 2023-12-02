from dataclasses import dataclass
import copy

lines = open("input.txt").read().split("\n")

# define number of cubes in bag for part 1
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

    # part 2 values:
    fewest_possible: CubeSet
    power_value: int

# Given an input line, return a populated Game object
def decode_game(line: str) -> Game:

    res = Game()

    # get game index
    index_str: str = line.split(":")[0][5:]
    index_int = int(index_str)
    res.id = index_int

    set_strs = line.split(":")[1].split(";")
    
    # input looks like " 4 red, 5 blue, 9 green"
    # outputs a CubeSet DataClass object
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

    # iterate through all sets and 
    # run through the above decode_set function
    sets: list[CubeSet] = []
    for set_str in set_strs:
        sets.append(decode_set(set_str))    
    res.sets = sets
    return res

# decode all games by iterating through each line in the input
def decode_all_games(lines: list[str]) -> list[Game]:
    res: list[Game] = []
    for line in lines:
        res.append(decode_game(line))
    return res

# filter out games that are not possible 
# given a total_num value for each color 
# of cube
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

# return the sum of all ids given a list of games
def sum_ids(games: list[Game]) -> int:
    sum = 0
    for game in games:
        sum += game.id
    return sum

# Part 2 specific functions:

# given a list of games, use the game.sets value to calulate
# the game.fewest_possible value
def calculate_fewest_possible_cubes(games: list[Game]) -> list[Game]:
    new_games = copy.copy(games)
    for game in new_games:
        min_red = 0
        min_green = 0
        min_blue = 0
        for set in game.sets:
            if set.red > min_red:
                min_red = set.red
            if set.green > min_green:
                min_green = set.green
            if set.blue > min_blue:
                min_blue = set.blue
        game.fewest_possible = CubeSet(min_red, min_green, min_blue)
    return new_games

# given a list of games where the fewest_possible value has already been 
# calculated (see calculate_fewest_possible_cubes function), calculate the
# power value
def calculate_power_values(games: list[Game]) -> list[Game]:
    new_games = copy.copy(games)
    for game in new_games:
       game.power_value = game.fewest_possible.red * game.fewest_possible.green * game.fewest_possible.blue
    return new_games 

# return the sum of all power_values given a list of games
def sum_power_values(games: list[Game]) -> int:
    sum = 0
    for game in games:
        sum += game.power_value
    return sum


# solutions:

def part_one(games: list[Game]) -> int:
    possible_games: list[Game] = get_only_possible_games(games, RED_LIMIT, GREEN_LIMIT, BLUE_LIMIT)
    return sum_ids(possible_games)


def part_two(games: list[Game]) -> int:
    transformed_games = calculate_fewest_possible_cubes(games)
    transformed_games = calculate_power_values(games)
    return sum_power_values(transformed_games)

games: list[Game] = decode_all_games(lines)

print("solution 1 {}".format(part_one(games)))
print("solution 2 {}".format(part_two(games)))



