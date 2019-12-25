#!python3
from collections import deque
from itertools import cycle, islice


def deal_into_new_stack(deck_of_cards):
    deck_of_cards.reverse()

def cut_cards(deck_of_cards, number):
    deck_of_cards.rotate(-number)

def deal_with_increment(deck_of_cards, number):
    new_deck = [x for x in range(0,len(deck_of_cards))]
    table_index = cycle(new_deck)
    new_deck[next(table_index)] = deck_of_cards.popleft()
    while len(deck_of_cards) > 0:
        card = deck_of_cards.popleft()
        index = next(islice(table_index, number-1, None), None)
        new_deck[index] = card
    return deque(new_deck.copy())


def execute_instructions(file):
    deck = deque([x for x in range(0,10007)])
    with open(file) as input_file:
        for line in input_file:
            instr = line.strip().split()
            if instr[0] == 'cut':
                cut_cards(deck, int(instr[-1]))
            elif instr[0] == 'deal':
                if instr[1] == 'with':
                    deck = deal_with_increment(deck, int(instr[-1]))
                elif instr[1] == 'into':
                    deal_into_new_stack(deck)
                else:
                    print('Unknown deal')
            else:
                print('Unknown instruction')

    return deck

shuffeled_deck = execute_instructions('input22.txt')
index = shuffeled_deck.index(2019)
print('Index for 2019: {}'.format(index))

"""
deck = deque([x for x in range(0,10)])

deal_into_new_stack(deck)
cut_cards(deck, -2)
deck = deal_with_increment(deck, 7)
cut_cards(deck, 8)
cut_cards(deck, -4)
deck = deal_with_increment(deck, 7)
cut_cards(deck, 3)
deck = deal_with_increment(deck, 9)
deck = deal_with_increment(deck, 3)
cut_cards(deck, -1)

print(deck)
"""
