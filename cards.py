import numpy as np
import itertools
import pandas as pd
from score import score_hand
import pickle
import helpers
from sys import getsizeof

def build_deck():
    numbers = list(range(2, 15))
    suits = ['H', 'S', 'C', 'D']
    deck = []
    for i in numbers:
        for s in suits:
            card = s+str(i)
            deck.append(card)
    return deck


def combinations(arr, n):
    """Returns all possible n-card combinations
    taking into account that order doesn’t matter in Poker
    """
    arr = np.asarray(arr)
    t = np.dtype([('', arr.dtype)]*n)
    result = np.fromiter(itertools.combinations(arr, n), t)
    return result.view(arr.dtype).reshape(-1, n)


def handvalues(combi):
    # iterate over all combinations scoring them
    scores = [{"hand": i, "value": score_hand(i, False)} for i in combi]
    # sort hands by score
    scores = sorted(scores, key=lambda k: k['value'])
    return scores


def all_hands_dataframe(hand_values):
    deck = build_deck()
    # making a list of hands
    x = [i.get("hand", "") for i in hand_values]
    # making a list of values
    y = [i.get("value", "") for i in hand_values]
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
