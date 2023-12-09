def get_numbers_from_line(line: str) -> list[int]:
    parts = line.split(" ")
    res: list[int] = []
    for part in parts:
        if part.lstrip('-').isnumeric():
            res.append(int(part))
    return res

def decode_input(input: str) -> list[list[int]]:
    res: list[list[int]] = []
    for line in input.split("\n"):
        res.append(get_numbers_from_line(line))
    return res

def get_diff_sequence(input: list[int]) -> list[int]:
    res: list[int] = []
    for i, number in enumerate(input):
        if i == 0:
            continue
        res.append(number - input[i-1])
    return res

def sequence_is_all_zeros(sequence: list[int]) -> bool:
    for number in sequence:
        if number != 0:
            return False
    return True

def get_diff_sequences_up_to_zero(base_sequence: list[int]) -> list[list[int]]:
    res: list[list[int]] = [base_sequence]
    while not sequence_is_all_zeros(res[-1]):
        res.append(get_diff_sequence(res[-1]))
    return res

def get_next_number_in_sequence(sequences_up_to_zero: list[list[int]]) -> int:
    res = 0
    for diff_sequence in sequences_up_to_zero:
        res += diff_sequence[-1]
    return res

def get_prev_number_in_sequence(sequences_up_to_zero: list[list[int]]) -> int:
    current_diff = 0
    for i, diff_sequence in enumerate(reversed(sequences_up_to_zero)):
        if i == 0:
            continue
        current_diff = diff_sequence[0] - current_diff
    return current_diff

txt_input = open("input.txt").read()
input = decode_input(txt_input)

def solve_part_one(input: list[list[int]]) -> int:
    res = 0
    for line in input:
        res += get_next_number_in_sequence(get_diff_sequences_up_to_zero(line))
    return res


def solve_part_two(input: list[list[int]]) -> int:
    res = 0
    for line in input:
        res += get_prev_number_in_sequence(get_diff_sequences_up_to_zero(line))
    return res

print("Part one solution: {}".format(solve_part_one(input)))
print("Part two solution: {}".format(solve_part_two(input)))

