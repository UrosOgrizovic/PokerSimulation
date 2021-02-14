import numpy as np
import itertools
import pandas as pd
from score import score_hand
import pickle
import helpers
from sys import getsizeof
from random import randint


def build_deck():
    """0 - 12 - hearts
    13 - 25 - spades
    26 - 38 - clubs
    39 - 51 - diamonds
    e.g. 0 = 2 of hearts, ..., 8 = 10H, 9 = 12H, 10 = 13H, 11 = 14H, 12 = ace of hearts
    13 = 2 of spades etc.

    Returns:
        list: list of cards, where each card is a number
    """
    return list(range(0, 52))


def get_random_card(used_cards):
    while True:
        card = randint(0, 51)
        if card not in used_cards:
            used_cards.append(card)
            return card


def combinations(arr, n):
    """Returns all possible n-card combinations
    taking into account that order doesn’t matter in Poker
    """
    return list(itertools.combinations(arr, n))


def handvalues(combi):
    # iterate over all combinations scoring them
    scores = [{"hand": i, "value": score_hand(i, False)} for i in combi]
    # sort hands by score
    scores = sorted(scores, key=lambda k: k['value'])
    return scores


def all_hands_dataframe(hand_values):
    deck = build_deck()
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
    # deck = build_deck()
    # c_5 = combinations(deck, 5)
    # hand_values = handvalues(c_5)
    # df = all_hands_dataframe(hand_values)

    # it's faster to use pickle than to generate objects every time
    # helpers.dump_object(deck, 'deck.pkl')
    # helpers.dump_object(c_5, 'c_5.pkl')
    # helpers.dump_object(hand_values, 'hand_values_c_5.pkl')
    # helpers.dump_object(df, 'all_hands_df.pkl')
    deck = helpers.load_object('deck.pkl')
    c_5 = helpers.load_object('c_5.pkl')
    hand_values = helpers.load_object('hand_values_c_5.pkl')
    df = helpers.load_object('all_hands_df.pkl')

    print(getsizeof(deck))
    print(getsizeof(c_5))
    print(getsizeof(hand_values))
    print(getsizeof(df))
