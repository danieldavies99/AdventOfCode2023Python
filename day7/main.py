from dataclasses import dataclass
from enum import Enum
input = open("input.txt").read().split("\n")

class TypePower(Enum):
    UNCALCULATED = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

@dataclass
class Hand:
    cards: list[str]
    bid: int
    type_power: TypePower
    order_rule_power: int

def get_card_int_val(card: str) -> int:
    vals: dict[str, int] = {"A": 13, "K": 12, "Q": 11, "J": 10, "T": 9, "9": 8, "8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2, "2": 1}
    return vals[card]

def get_card_int_val_part_two(card: str) -> int:
    vals: dict[str, int] = {"A": 13, "K": 12, "Q": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "J": 1,}
    return vals[card]


def decode_input(input: list[str]) -> list[Hand]:
    print(input)
    res: list[Hand] = []
    for line in input:
        parts = line.split(" ")
        res.append(
            Hand(
                [parts[0][0], parts[0][1], parts[0][2], parts[0][3], parts[0][4]],
                int(parts[1]),
                TypePower.UNCALCULATED,
                0
            )
        )
    return res

# returns the count of the highest matches cards
# returns matching counts
# 1 1 3 3 3 returns [3, 2]
# 5 5 5 5 5 returns [5]
# 1 2 3 4 5 returns [1, 1, 1, 1, 1]
# etc.
# highest count will always return first
def get_match_counts(hand: Hand) -> list[int]:
    matches: dict[str, int] = {"A": 0, "K": 0, "Q": 0, "J": 0, "T": 0, "9": 0, "8": 0, "7": 0, "6": 0, "5": 0, "4": 0, "3": 0, "2": 0}
    for card in hand.cards:
        matches[card] += 1
    int_matches = []
    for match_count in matches.values():
        if match_count > 0:
            int_matches.append(match_count)
    int_matches.sort(reverse=True)
    return int_matches

# returns the count of the highest matches cards
# returns matching counts
# 1 1 3 3 3 returns [3, 2]
# 5 5 5 5 J returns [5]
# 1 2 3 4 J returns [2, 1, 1, 1, 1]
# etc.
# highest count will always return first
# J matches get added to highest match
def get_match_counts_part_two(hand: Hand) -> list[int]:
    matches: dict[str, int] = {"A": 0, "K": 0, "Q": 0, "J": 0, "T": 0, "9": 0, "8": 0, "7": 0, "6": 0, "5": 0, "4": 0, "3": 0, "2": 0}
    for card in hand.cards:
        matches[card] += 1
    int_matches = []
    for card, match_count in matches.items():
        if match_count > 0 and card != "J":
            int_matches.append(match_count)
    int_matches.sort(reverse=True)
    if len(int_matches) == 0: # account for possibility of JJJJJ hand
        return [5]
    int_matches[0] += matches["J"]
    return int_matches

def has_five_of_a_kind(hand: Hand, part_two: bool) -> bool:
    if part_two:
        return get_match_counts_part_two(hand)[0] == 5
    return get_match_counts(hand)[0] == 5

def has_four_of_a_kind(hand: Hand, part_two: bool) -> bool:
    if part_two:
        return get_match_counts_part_two(hand)[0] == 4
    return get_match_counts(hand)[0] == 4

def has_full_house(hand: Hand, part_two: bool) -> bool:
    if part_two:
        return get_match_counts_part_two(hand)[0] == 3 and get_match_counts_part_two(hand)[1] == 2
    return get_match_counts(hand)[0] == 3 and get_match_counts(hand)[1] == 2

def has_three_of_a_kind(hand: Hand, part_two: bool) -> bool:
    if part_two:
        return get_match_counts_part_two(hand)[0] == 3
    return get_match_counts(hand)[0] == 3

def has_two_pair(hand: Hand, part_two: bool) -> bool:
    if part_two:
        return get_match_counts_part_two(hand)[0] == 2 and get_match_counts_part_two(hand)[1] == 2
    return get_match_counts(hand)[0] == 2 and get_match_counts(hand)[1] == 2

def has_one_pair(hand: Hand, part_two: bool) -> bool:
    if part_two:
        return get_match_counts_part_two(hand)[0] == 2
    return get_match_counts(hand)[0] == 2

def has_high_card(hand: Hand, part_two: bool) -> bool:
    if part_two:
        return get_match_counts_part_two(hand)[0] == 1
    return get_match_counts(hand)[0] == 1

# sets the type power of given hand
# mutates the hand object directly via reference
def calc_type_power(hand: Hand, part_two: bool) -> None:
    if has_five_of_a_kind(hand, part_two):
        hand.type_power = TypePower.FIVE_OF_A_KIND
        return
    if has_four_of_a_kind(hand, part_two):
        hand.type_power = TypePower.FOUR_OF_A_KIND
        return
    if has_full_house(hand, part_two):
        hand.type_power = TypePower.FULL_HOUSE
        return
    if has_three_of_a_kind(hand, part_two):
        hand.type_power = TypePower.THREE_OF_A_KIND
        return
    if has_two_pair(hand, part_two):
        hand.type_power = TypePower.TWO_PAIR
        return
    if has_one_pair(hand, part_two):
        hand.type_power = TypePower.ONE_PAIR
        return
    if has_high_card(hand, part_two):
        hand.type_power = TypePower.HIGH_CARD
        return
    print("something has definitely gone wrong")

def calc_order_rule_power(hand: Hand, part_two: bool) -> None:
    string_res = ""
    for card in hand.cards:
        string_rep = str(get_card_int_val(card)) if not part_two else str(get_card_int_val_part_two(card))
        if(len(string_rep) == 1):
            string_rep = "0" + string_rep
        string_res += string_rep
    hand.order_rule_power = int(string_res)

def solve_part_one(hands: list[Hand]) -> int:
    for hand in hands:
        calc_type_power(hand, False)
        calc_order_rule_power(hand, False)

    sorted_hands = sorted(hands, key = lambda x: (x.type_power.value, x.order_rule_power))
    res = 0
    for i, hand in enumerate(sorted_hands):
        res += hand.bid * (i + 1)
        print("{}, {}, {}: {}*{}".format("".join(hand.cards), hand.type_power, hand.order_rule_power, hand.bid, i + 1))
    return res

def solve_part_two(hands: list[Hand]) -> int:
    for hand in hands:
        calc_type_power(hand, True)
        calc_order_rule_power(hand, True)

    sorted_hands = sorted(hands, key = lambda x: (x.type_power.value, x.order_rule_power))
    res = 0
    for i, hand in enumerate(sorted_hands):
        res += hand.bid * (i + 1)
        print("{}, {}, {}: {}*{}".format("".join(hand.cards), hand.type_power, hand.order_rule_power, hand.bid, i + 1))
    return res

hands = decode_input(input)

print("Part one {}".format(solve_part_one(hands)))
print("Part two {}".format(solve_part_two(hands)))
