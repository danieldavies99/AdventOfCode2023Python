from dataclasses import dataclass
lines = open("input.txt").read().split("\n")

MAP_HEIGHT = len(lines)
MAP_WIDTH = len(lines[0])
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
NUMBERS_WITH_PERIOD = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']

@dataclass
class Position:
    x: int
    y: int

    def __key(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.__key() == other.__key()
        return NotImplemented

# Decode input into a list of a list of characters that will represent
# the "map" object. Note that if reading directly from map you need to read 
# in the form map[y][x] (y is switched with x) and larger values of y equate
# lower positions in the map if you were thinking of it in terms of cartesian 
# coords
# 
# (2, 0):
# . . @
# . . .
# . . .
#
# (0, 2)
# . . .
# . . .
# @ . . 
def decode_input(lines: list[str]) -> list[list[str]]:
    res: list[list[str]] = []

    for line in lines:
        current_line = []
        for character in line:
            current_line.append(character)
        res.append(current_line)

    return res

# Check that a position falls within the bounds of the map
def position_is_in_map(position: Position, map_width: int, map_height: int) -> bool:
    return position.x >= 0 and position.x < map_width - 1 and position.y >= 0 and position.y < map_height - 1

# get the character at a given x/y position on the map
def get_symbol_at_point(position: Position, map: list[list[str]]) -> str:
    return map[position.y][position.x]

# get all the neighboring points of a give position, excluding those that would fall
# outside the bounds of the map
def get_neighboring_points(position: Position, map: list[list[str]]) -> dict[str, str]:
    def add_positions_to_dict(positions: list[Position]):
        res = {}
        for position in positions:
            if position_is_in_map(position, MAP_WIDTH, MAP_HEIGHT):
                res[position] = get_symbol_at_point(position, map)
        return res

    return add_positions_to_dict([
        Position(position.x-1, position.y), # left
        Position(position.x-1, position.y+1), # bottom left
        Position(position.x, position.y+1), # bottom
        Position(position.x+1, position.y+1), # bottom right
        Position(position.x+1, position.y), # right
        Position(position.x+1, position.y-1), # top right
        Position(position.x, position.y-1), # top
        Position(position.x-1, position.y-1), # top left
    ])

# find all numbers in the map and return them as ints along with the positions
# of each of their individual characters
def find_all_numbers(map: list[list[str]]) -> list[tuple[int, list[Position]]]:
    res = []
    num_accumulator: str = ''
    pos_accumulator: list[Position] = []
    def is_number(input: str) -> bool:
        return input[0] in NUMBERS
    for y, line in enumerate(map):
        for x, tile in enumerate(line):
            if is_number(tile):
                num_accumulator += tile
                pos_accumulator.append(Position(x, y))
            else:
                if len(num_accumulator) > 0:
                    res.append((int(num_accumulator), pos_accumulator))
                    num_accumulator = ''
                    pos_accumulator = []
        # numbers can't span lines
        if len(num_accumulator) > 0:
            res.append((int(num_accumulator), pos_accumulator))
            num_accumulator = ''
            pos_accumulator = []
    return res

# given a number and it's positions, determine if it is neighboring a part
def number_is_neighboring_a_part(number_with_positions: tuple[int, list[Position]], map: list[list[str]]) -> bool:
    for position in number_with_positions[1]:
        neighbors = get_neighboring_points(position, map)
        for neighbor in neighbors:
            tile = get_symbol_at_point(neighbor, map)
            if tile not in NUMBERS_WITH_PERIOD:
                return True
    return False

# Part 2 specific functions:

# find the positions of all * symbols in the map
def find_all_gear_symbols(map: list[list[str]]) -> list[Position]:
    res = []
    for y, line in enumerate(map):
        for x, tile in enumerate(line):
            if tile == "*":
                res.append(Position(x, y))
    return res

# for each gear symbol, return all numbers that it neighbors
def get_numbers_that_neighbor_position(
        position: Position,
        map: list[list[str]],
        numbers_with_positions: list[tuple[int, list[Position]]]
    ) -> list[int]:
    res = []
    gear_neighbors = get_neighboring_points(position, map)
    for number_with_position in numbers_with_positions:
        neighbors = False
        for position in number_with_position[1]:
            for neighbor in gear_neighbors:
                if position == neighbor:
                    neighbors = True
        if neighbors:
            res.append(number_with_position[0])
    return res

# solutions:

# solve part one
def solve_part_one(map: list[list[str]]) -> int:
    sum = 0
    numbers_with_positions = find_all_numbers(map)
    for number_with_position in numbers_with_positions:
        if number_is_neighboring_a_part(number_with_position, map):
            sum += number_with_position[0]
    return sum

# solve part two
def solve_part_two(map: list[list[str]]) -> int:
    sum = 0
    numbers_with_positions = find_all_numbers(map)
    gear_symbol_positions = find_all_gear_symbols(map)
    for position in gear_symbol_positions:
        numbers = get_numbers_that_neighbor_position(position, map, numbers_with_positions)
        if len(numbers) == 2:
            sum += numbers[0] * numbers[1]
    return sum

map: list[list[str]] = decode_input(lines)
print("Solution Part One {}".format(solve_part_one(map)))
print("Solution Part Two {}".format(solve_part_two(map))) 
