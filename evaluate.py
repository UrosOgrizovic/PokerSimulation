from cards import c_5, combinations, df
from score import score_hand
from numba import jit
import numpy as np
from functools import lru_cache


def should_call(players, percentile, pot, price):
    pwin = (percentile/100)**players
    ev = pwin*pot
    if ev - price <= 0:
        print('You should fold')
    if ev - price > 0:
        print('You should bet')
    print('The expected value betting %s is %s $' % (price, ev-price))
    return pwin*100


@jit(nopython=True)
def common(a, b):
    # common = []
    # l1 = [i for i in a]
    # l2 = [i for i in b]
    # common = len([i for i in l1 if i in l2])
    return len([i for i in a if i in b])


@jit(nopython=True)
def numba(c_n, c_5):
    results = []
    len1 = c_n.shape[0]
    len2 = c_5.shape[0]
    for i in range(len1):
        for j in range(len2):
            if common(c_n[i], c_5[j]) == 4:
                results.append(c_5[j])
    return results


@lru_cache(maxsize=None)
def opti(c_n, c_5):
    values = numba(c_n, c_5)
    return [score_hand(i) for i in values]


def expected_value(hand, c_3, c_4, c_5):
    # maxi is for current, mean is for future
    if len(hand) == 5:
        maxi = score_hand(hand)
        mean = np.mean(opti(c_3, c_5) + opti(c_4, c_5))
    elif len(hand) == 6:
        maxi = max([score_hand(i) for i in combinations(hand, 5)])
        mean = np.mean(opti(c_4, c_5))
    elif len(hand) == 7:
        maxi = max([score_hand(i) for i in combinations(hand, 5)])
        mean = maxi
    values = [maxi, mean]
    return values


flop = []

for i in range(0, 5):
    flop.append(str(input('enter card: ')))
c_4 = combinations(flop, 4)
c_3 = combinations(flop, 3)
flopscore = expected_value(flop, c_3, c_4, c_5)
current = df.loc[df['value'] >= flopscore[0]].index[0]/2598960*100
future = df.loc[df['value'] >= flopscore[1]].index[1]/2598960*100
print(f'Current value is  {current} and the avg expected value is {future}')
players = float(input('enter number of players: '))
pot = float(input('enter pot value: '))
price = float(input('enter value of your bet: '))
if current > future:
    should_call(players, current, pot, price)
else:
    should_call(players, future, pot, price)
