import pickle
import itertools
import os


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


def get_q_values_path(is_sarsa, policy_name):
    if is_sarsa:
        q_values_path = f'q_values_sarsa_{policy_name}.pkl'
    else:   # Q-learning
        q_values_path = f'q_values_ql.pkl'
    return q_values_path


def initialize_q():
    states = load_object('states.pkl')
    q = {state: {'bet': 0.0, 'fold': 0.0} for state in states}
    return q


def get_q_values_object(q_values_path):
    if os.path.exists(q_values_path):
        q = load_object(q_values_path)
    else:
        q = initialize_q()
    return q