from dataclasses import dataclass
import copy
maps_input = open("input.txt").read().split("\n\n")

@dataclass
class MapSection:
    dest_range_start: int
    source_range_start: int
    range_length: int

@dataclass
class Map:
    sections: list[MapSection]

def get_numbers_from_line(line: str) -> list[int]:
    parts = line.split(" ")
    res: list[int] = []
    for part in parts:
        if part.isnumeric():
            res.append(int(part))
    return res

def decode_map_from_string(map_input: str) -> Map:
    lines = map_input.split('\n')
    # remove first line ("seed-to-soil-map:")
    lines.pop(0)
    sections: list[MapSection] = []
    for line in lines:
        numbers = get_numbers_from_line(line)
        sections.append(MapSection(numbers[0], numbers[1], numbers[2]))
    return Map(sections)

def decode_all_maps(raw_input: list[str]) -> list[Map]:
    input_copy = copy.copy(raw_input)
    # get rid of seeds list
    input_copy.pop(0)
    res: list[Map] = []
    for map_string in input_copy:
        res.append(decode_map_from_string(map_string))
    return res

def get_mapped_value(number: int, map: Map) -> int:
    for section in map.sections:
        if number >= section.source_range_start and number < section.source_range_start + section.range_length:
            diff = number - section.source_range_start
            return section.dest_range_start + diff
    return number


def get_lowest_number_in_list(input: list[int]) -> int:
    lowest_val = input[0]

    for val in input:
        if val < lowest_val:
            lowest_val = val
    return lowest_val

def get_all_seed_numbers(seed_ranges: list[int]):
    res = []
    seed_index = 0
    while seed_index < len(seed_ranges):
        for i in range(seed_ranges[seed_index],seed_ranges[seed_index] + seed_ranges[seed_index+1]):
            res.append(i)
        seed_index += 2
    return res


def solve_part_one(maps: list[Map]) -> int:
    start_seeds = get_numbers_from_line(maps_input[0])

    final_location_values: list[int] = []
    for seed in start_seeds:
        seed_val = copy.copy(seed)
        for map in maps:
            seed_val = get_mapped_value(seed_val, map)
        final_location_values.append(seed_val)
    return get_lowest_number_in_list(final_location_values)

# technically would work, but takes far too long to run
# I will come back to this
# def solve_part_two(maps: list[Map]) -> int:
#     start_seeds = get_all_seed_numbers(get_numbers_from_line(maps_input[0]))
#     print("num starting seeds: {}".format(len(start_seeds)))

#     final_location_values: list[int] = []
#     for seed in start_seeds:
#         seed_val = copy.copy(seed)
#         for map in maps:
#             seed_val = get_mapped_value(seed_val, map)
#         final_location_values.append(seed_val)
#     return get_lowest_number_in_list(final_location_values)


maps = decode_all_maps(maps_input)
print("Part one solution: {}".format(solve_part_one(maps)))
# print("Part two solution: {}".format(solve_part_two(maps)))
