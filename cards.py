import numpy as np
import pandas as pd
from score import score_hand
import pickle
import helpers
from sys import getsizeof
from random import choice
from constants import DECK


def get_random_card(used_cards):
    """Get a random card that wasn't already used

    Args:
        used_cards (set)

    Returns:
        (int): a card
    """
    while True:
        card = choice(DECK)
        if card not in used_cards:
            used_cards.add(card)
            return card


def handvalues(combinations):
    # iterate over all combinations scoring them
    scores = {comb: score_hand(comb, False) for comb in combinations}
    return scores


if __name__ == '__main__':
    c_2 = helpers.combinations(DECK, 2)
    # c_5 = helpers.combinations(DECK, 5)
    # states = c_2 + c_5
    # hand_values = handvalues(c_5)

    # it's faster to use pickle than to generate objects every time
    # helpers.dump_object(c_2, 'c_2.pkl')
    # helpers.dump_object(c_5, 'c_5.pkl')
    # helpers.dump_object(states, 'states.pkl')
    # helpers.dump_object(hand_values, 'hand_values_c_5.pkl')

    # c_5 = helpers.load_object('c_5.pkl')
    # hand_values = helpers.load_object('hand_values_c_5.pkl')

    # print(getsizeof(c_5))
    # print(getsizeof(hand_values))
