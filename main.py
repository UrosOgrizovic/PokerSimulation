import numpy as np
from constants import deck, c_5, all_hands_df, TOTAL_NUM_COMBINATIONS, NUM_PLAYERS
from cards import get_random_card, combinations
import helpers
from evaluate import expected_value, should_call
from score import score_hand

def sarsa_q_learning(q, s, a, alpha, r, gamma, s_prime, player_score, is_sarsa=True, policy_name='greedy'):
    """
    SARSA - on-policy temporal difference algorithm
    q(s, a) = q(s, a) + alpha * (r + gamma * q(s', a') - q(s, a))

    Q-learning - similar to sarsa; the only difference is that
    sarsa employs the given policy to get the new value (a_prime),
    whereas q-learning always uses the greedy policy for that
    same task.
    q(s, a) = q(s, a) + alpha * (r + gamma * max(a')(q(s', a')) - q(s, a))

    it runs after each move

    :param q: all q-values
    :param s: old state
    :param a: old action
    :param alpha: learning rate
    :param r: reward
    :param gamma: discount factor
    :param s_prime: new state
    :param player_score: current player score
    :param is_sarsa: True (sarsa) or False (q-learning)
    :param policy_name: name of policy
    :return:
    """
    if is_sarsa:
        a_prime = get_action_by_policy_name(q, s_prime, policy_name)
    else:
        a_prime = greedy_policy(q[player_score])  # use greedy policy for q-learning

    new_q_value = 0  # all terminal nodes are initialized to zero
    if s_prime < 21:
        new_q_value = q[s_prime][a_prime]

    q[s][a] = q[s][a] + alpha * (r + gamma * new_q_value - q[s][a])
    return q


def simulate_flop(used_cards, cards_on_table, player_hand, states_actions):
    # TODO: implement
    for i in range(3):
        cards_on_table.append(get_random_card(used_cards))
    cards_on_table.extend(player_hand)
    c_3 = tuple([tuple(comb) for comb in combinations(cards_on_table, 3)])
    c_4 = tuple([tuple(comb) for comb in combinations(cards_on_table, 4)])
    flopscore = expected_value(cards_on_table, c_3, c_4)
    current = all_hands_df.loc[all_hands_df['value'] >= flopscore[0]].index[0]/TOTAL_NUM_COMBINATIONS
    future = all_hands_df.loc[all_hands_df['value'] >= flopscore[1]].index[0]/TOTAL_NUM_COMBINATIONS
    bet_fold = ''
    # TODO: use QL instead of should_call to determine what to do
    if current > future:
        bet_fold = should_call(NUM_PLAYERS, current)
    else:
        bet_fold = should_call(NUM_PLAYERS, future)
    states_actions[c_5.index(cards)] = bet_fold


def simulate_turn(used_cards, cards_on_table, player_hand, states_actions):
    cards_on_table.append(get_random_card(used_cards))
    cards_on_table.extend(player_hand)
    c_4 = tuple([tuple(comb) for comb in combinations(cards_on_table, 4)])
    combiturn = expected_value(cards_on_table, None, c_4)
    current = all_hands_df.loc[all_hands_df['value'] >= combiturn[0]].index[0]/TOTAL_NUM_COMBINATIONS
    future  = all_hands_df.loc[all_hands_df['value'] >= combiturn[1]].index[0]/TOTAL_NUM_COMBINATIONS
    bet_fold = ''
    if  current > future:
        bet_fold = should_call(NUM_PLAYERS, current)
    else:
        bet_fold = should_call(NUM_PLAYERS, future)
    states_actions[c_5.index(cards)] = bet_fold


def simulate_river(used_cards, cards_on_table, player_hand, states_actions):
    cards_on_table.append(get_random_card(used_cards))
    cards_on_table.extend(player_hand)
    combiriver = expected_value(cards_on_table, None, None)
    current = all_hands_df.loc[all_hands_df['value'] >= combiriver[0]].index[0]/TOTAL_NUM_COMBINATIONS
    bet_fold = should_call(current)
    states_actions[c_5.index(cards)] = bet_fold
    return current


def simulate_game(q):
    used_cards = []
    cards_on_table = []
    states_actions = []
    hand1 = (get_random_card(used_cards), get_random_card(used_cards))
    hand2 = (get_random_card(used_cards), get_random_card(used_cards))
    simulate_flop(used_cards, cards_on_table, hand1, states_actions)
    simulate_turn(used_cards, cards_on_table, hand1, states_actions)
    val1 = simulate_river(used_cards, cards_on_table, hand1, states_actions)
    val2 = simulate_river(used_cards, cards_on_table, hand2, states_actions)
    print(used_cards)
    print(hand1, val1)
    print(hand2, val2)
    print(cards_on_table)
    print('Game over')
    if val1 > val2:
        for state, action in states_actions:
            q[state][action] += 0.5
    elif val1 < val2:
        for state, action in states_actions:
            q[state][action] -= 0.5
    print(max(q.values()))
    '''TODO:
    1. flop
    2. turn
    3. river
    4. update state values (SARSA, Q-learning, TDL, Monte Carlo)
    '''


if __name__ == '__main__':
    ''' q values format:
    state (type: list) - current hand consisting of 5 cards
    action (type: dict) - how good is each possible action {'bet': value, 'fold': value}
    '''
    # q = helpers.load_object('q_values.pkl')
    print(len(c_5))
    # use index in c_5 as key because lists and np.arrays are unhashable, i.e. can't be used as keys
    q = {i: {'bet': 0.0, 'fold': 0.0} for i in range(len(c_5))}
    num_games = 10
    simulate_game(q)
    # for i in range(num_games):
    #     simulate_game(q)
    # helpers.dump_object(q, 'q_values.pkl')