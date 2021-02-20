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


def handvalues(combi):
    # iterate over all combinations scoring them
    scores = [{"hand": i, "value": score_hand(i, False)} for i in combi]
    # sort hands by score
    scores = sorted(scores, key=lambda k: k['value'])
    return scores


def all_hands_dataframe(hand_values):
    # making a list of hands
    x = [i.get("hand") for i in hand_values]
    # making a list of values
    y = [i.get("value") for i in hand_values]
    # making a dictionary of hands and values
    data = {'hands': x, 'value': y}
    # making a pandas dataframe with hands and values
    df = pd.DataFrame(data)
    return df


if __name__ == '__main__':
    c_2 = helpers.combinations(DECK, 2)
    # c_5 = helpers.combinations(DECK, 5)
    # states = c_2 + c_5
    # hand_values = handvalues(c_5)
    # df = all_hands_dataframe(hand_values)

    # it's faster to use pickle than to generate objects every time
    # helpers.dump_object(c_2, 'c_2.pkl')
    # helpers.dump_object(c_5, 'c_5.pkl')
    # helpers.dump_object(states, 'states.pkl')
    # helpers.dump_object(hand_values, 'hand_values_c_5.pkl')
    # helpers.dump_object(df, 'all_hands_df.pkl')

    # c_5 = helpers.load_object('c_5.pkl')
    # hand_values = helpers.load_object('hand_values_c_5.pkl')
    # df = helpers.load_object('all_hands_df.pkl')

    # print(getsizeof(c_5))
    # print(getsizeof(hand_values))
    # print(getsizeof(df), len(df))
