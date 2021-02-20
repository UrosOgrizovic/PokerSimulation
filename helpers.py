import pickle
import itertools

def dump_object(object, path):
    with open(path, 'wb') as f:
        pickle.dump(object, f, protocol=2)


def load_object(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj


def combinations(arr, n):
    """Returns all possible n-card combinations
    taking into account that order doesn’t matter in Poker
    """
    return tuple(sorted(itertools.combinations(arr, n)))
