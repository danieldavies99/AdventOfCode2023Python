from dataclasses import dataclass
import copy
lines = open("input.txt").read().split("\n")

@dataclass
class Card:
    id: int
    winners: list[int]
    chances: list[int]

    # part 2
    has_been_processed: bool

def decode_input(lines: list[str]) -> list[Card]:
    def decode_line(line: str) -> Card:
        # get rid of colon character
        # which prevents isnumeric
        # from findng the id
        line = line.replace(":", "")

        parts = line.split("|")
        id = -1
        winners: list[int] = []
        chances: list[int] = []
        # decode winners
        for part in parts[0].split(' '):
            if part.isnumeric() and id == -1:
                id = int(part)
                continue
            if part.isnumeric():
                winners.append(int(part))
        for part in parts[1].split(' '):
            if part.isnumeric():
                chances.append(int(part))
        return Card(id, winners, chances, False)

    res = []
    for line in lines:
        res.append(decode_line(line))
    return res

def get_winning_numbers(card: Card) -> list[int]:
    winners: list[int] = []
    for winning_numer in card.winners:
        for chance in card.chances:
            if chance == winning_numer:
                winners.append(chance)
    return winners

def get_score_from_num_winner(num_winners: int) -> int:
    if num_winners == 0:
        return 0
    sum = 1
    for i in range(num_winners - 1):
        sum *= 2
    return sum

def get_copy_of_card(original_cards: list[Card], card_id: int) -> Card:
    return copy.copy(original_cards[card_id - 1])


# Part 2 specific functions:
def process_copies(original_cards: list[Card], copies: list[Card]) -> tuple[bool, list[Card]]:
    has_won_cards = False
    new_cards = []
    new_cards.extend(copy.copy(copies))
    for card_copy in copies:
        if card_copy.has_been_processed:
            continue
        num_winners = len(get_winning_numbers(card_copy))
        for i in range(num_winners):
            has_won_cards = True
            new_card_id = card_copy.id + 1 + i
            # if(new_card_id > len(original_cards) + 1):
            #     continue
            new_card = get_copy_of_card(original_cards, new_card_id)
            new_card.has_been_processed = False
            new_cards.append(new_card)
            # print("won copy {}".format(new_card.id))
        card_copy.has_been_processed = True
    return has_won_cards, new_cards

# Solutions

# very slow recursive approach, does work but takes over a minute
# I could definitely optimize this but I can't be bothered
def solve_part_2(cards: list[Card]) -> int:
    has_won_cards = True
    copies = copy.copy(cards)
    tracker = 0
    while has_won_cards:
        tracker += 1
        has_won_cards, copies = process_copies(cards, copies)
        print("iteration", tracker)
        # print(has_won_cards, copies, "\n")

    return len(copies)

def solve_part_1(cards: list[Card]) -> int:
    total_value: int = 0
    for card in cards:
        score = get_score_from_num_winner(len(get_winning_numbers(card)))
        # print("card {}, score {}".format(card.id, score))
        total_value += score
    return total_value

cards = decode_input(lines)
print("Part one: {}".format(solve_part_1(cards)))
print("Part two: {}".format(solve_part_2(cards)))

