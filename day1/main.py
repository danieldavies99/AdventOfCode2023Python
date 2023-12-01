lines = open("input.txt").read().split("\n")

# Return the first and last digits found in a string
# e.g. 1sldkfje4ldlkjf -> 1, 4
# e.g. asldj3lasdkjf -> 3, 3
def get_digits(line: str) -> (int, int):
    all_ints: list[int] = []
    for character in line:
        if not character.isnumeric():
            continue
        all_ints.append(int(character))
    first_digit = all_ints[0]
    # Ternary operator, how fancy
    last_digit = all_ints[-1] if len(all_ints) > 1 else all_ints[0]
    return first_digit, last_digit

# Combine two ints and return the int value as if int1 is the tens and int2 is the ones value
# e.g. 1, 2 -> 12
def combine_digits(num1: int, num2: int) -> int:
    return int(str(num1) + str(num2))

# Get solution for part 1
def part_one(lines: list[str]) -> int:
    sum: int = 0
    for line in lines:
        # get_digits returns two ints, combine_digits takes two ints as input
        # so we can use the expansion operator * to feed one function directly into the next
        sum += combine_digits(*get_digits(line))
    return sum

# Part 2 specific functions:

# replace any string numbers e.g. "one" to their single digit numeric representation e.g. "1"
def replace_string_digits(line: str) -> str:
    strings_to_ints = {
        "oneight": "18", # doubles have to go first, otherwise they'll be replaced by the singles
        "twone": "21",
        "threeight": "38",
        "fiveight": "58",
        "sevenine": "79",
        "eightwo": "82",
        "eighthree": "83",
        "nineight": "98",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    def replace_all(text: str, dic: dict[str, str]):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text
    return replace_all(line, strings_to_ints)

# replace all strings with their single digit numeric representations
# given a list of strings
def replace_all_string_digits(lines: list[str]) -> list[str]:
    res: list[str] = []
    for line in lines:
        res.append(replace_string_digits(line))
    return res

# Get solution for part 2
def part_two(lines: list[str]) -> int:
    sum: int = 0
    transformed_lines = replace_all_string_digits(lines)
    for line in transformed_lines:
        sum += combine_digits(*get_digits(line))
    return sum

# Print solutions
print("Part One Total: {}".format(part_one(lines)))
print("Part Two total: {}".format(part_two(lines)))
