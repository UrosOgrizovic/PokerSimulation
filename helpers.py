import pickle
import os
import numpy as np
import pandas as pd
from score import score_hand, handvalues
from constants import DECK
from cards import combinations


def dump_object(object, path):
    with open(path, 'wb') as f:
        pickle.dump(object, f, protocol=2)


def load_object(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            obj = pickle.load(f)
        return obj
    else:
        print(f'File on path {path} does not exist. Creating file and returning None.')
        open(path, 'w').close()
        return None


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


def initialize_files():
    file_names = ['c_2.pkl', 'c_5.pkl', 'states.pkl', 'hand_values_c_5.pkl']
    c_2, c_5 = load_object('c_2.pkl'), load_object('c_5.pkl')
    states = load_object('states.pkl')
    hand_values = load_object('hand_values_c_5.pkl')

    should_dump = False
    if c_2 is None or c_5 is None or states is None or hand_values is None
        should_dump = True

    c_2 = combinations(DECK, 2) if c_2 is None else c_2
    c_5 = combinations(DECK, 5) if c_5 is None else c_5
    states = c_2 + c_5 if states is None else states
    hand_values = handvalues(c_5) if hand_values is None else hand_values

    objects = [c_2, c_5, states, hand_values]
    if should_dump:
        for i in range(len(objects)):
            dump_object(objects[i], file_names[i])
