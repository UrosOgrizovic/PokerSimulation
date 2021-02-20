from helpers import combinations
from constants import c_5, all_hands_df, TOTAL_NUM_COMBINATIONS, NUM_PLAYERS
from score import score_hand
from numba import jit
import numpy as np
from functools import lru_cache


def should_call(percentile):
    pwin = percentile - NUM_PLAYERS * 0.05
    to_ret = 'bet'
    if pwin <= 0.7:
        print('You should fold')
        to_ret = 'fold'
    else:
        print('You should bet')
    return to_ret


@jit(nopython=True)
def common(a, b):
    common = []
    l1 = [i for i in a]
    l2 = [i for i in b]
    common = len([i for i in l1 if i in l2])
    return common


@jit(nopython=True)
def numba_4(c_4, c_5):
    results = []
    len1 = np.array(c_4).shape[0]
    len2 = np.array(c_5).shape[0]
    for i in range(len1):
        for j in range(len2):
            if common(c_4[i], c_5[j]) == 4:
                results.append(c_5[j])
    return results


@jit(nopython=True)
def numba_3(c_3, c_5):
    results = []
    len1 = np.array(c_3).shape[0]
    len2 = np.array(c_5).shape[0]
    for i in range(len1):
        for j in range(len2):
            if common(c_3[i], c_5[j]) == 4:
                results.append(c_5[j])
    return results


@lru_cache(maxsize=None)
def opti_3(c_3, c_5):
    values = numba_3(list(c_3), list(c_5))
    return [score_hand(i, False) for i in values]


@lru_cache(maxsize=None)
def opti_4(c_4, c_5):
    values = numba_4(list(c_4), list(c_5))
    return [score_hand(i, False) for i in values]


def expected_value(hand, c_3, c_4, c_5):
    if len(hand) == 5:  # flop
        maxi = score_hand(hand, False)
        mean = np.mean(opti_3(c_3, c_5) + opti_4(c_4, c_5))
    elif len(hand) == 6:    # turn
        maxi = max([score_hand(i, False) for i in combinations(hand, 5)])
        mean = np.mean(opti_4(c_4, c_5))
    elif len(hand) == 7:    # river
        maxi = max([score_hand(i, False) for i in combinations(hand, 5)])
        mean = maxi
    values = [maxi, mean]
    return values


if __name__ == '__main__':
    # FLOP
    flop = [10, 14, 11, 12, 3]

    c_5 = np.array(c_5)
    c_4 = np.array(combinations(flop, 4))
    c_3 = np.array(combinations(flop, 3))
    flopscore = expected_value(flop, c_3, c_4, c_5)
    print(f'Flopscore {flopscore}')
    current = all_hands_df.loc[all_hands_df['value'] >= flopscore[0]].index[0]/TOTAL_NUM_COMBINATIONS
    future = all_hands_df.loc[all_hands_df['value'] >= flopscore[1]].index[0]/TOTAL_NUM_COMBINATIONS
    print(f'Current value is  {current} and the avg expected value is {future}')
    if current > future:
        should_call(current)
    else:
        should_call(future)

    # TURN
    flop.append(13)
    c4 = np.array([sorted(i) for i in combinations(flop, 4)])
    combiturn = expected_value(flop, c_3, c_4, c_5)
    current = all_hands_df.loc[all_hands_df['value'] >= combiturn[0]].index[0]/TOTAL_NUM_COMBINATIONS
    future  = all_hands_df.loc[all_hands_df['value'] >= combiturn[1]].index[0]/TOTAL_NUM_COMBINATIONS
    print('My current value is %s and the average future value is %s' % (current, future))

    if  current > future:
        should_call(current)
    else:
        should_call(future)

    # RIVER
    flop.append(42)
    combiriver = expected_value(flop, c_3, c_4, c_5)
    current = all_hands_df.loc[all_hands_df['value'] >= combiriver[0]].index[0]/TOTAL_NUM_COMBINATIONS
    print('My final value is %s' % current)
    decision = should_call(current)
    print(f'Decision {decision}')