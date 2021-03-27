import numpy as np
import pandas as pd
import pickle
from sys import getsizeof
from random import choice
from constants import DECK
import itertools


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


def combinations(arr, n):
    """Returns all possible n-card combinations
    taking into account that order doesn’t matter in Poker
    """
    return tuple(sorted(itertools.combinations(arr, n)))
