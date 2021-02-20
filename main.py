import numpy as np
from constants import DECK, c_5, all_hands_df, TOTAL_NUM_COMBINATIONS, NUM_PLAYERS, ALPHA,\
                      GAMMA, STATES, DECK_DICTIONARY
from cards import get_random_card
import helpers
from evaluate import expected_value, should_call
from score import score_hand, score_hands
from policy import greedy_policy, eps_greedy_policy, softmax_policy,\
                   get_action_by_policy_name


def sarsa_q_learning(q, s, a, alpha, r, gamma, s_prime, is_sarsa=True, policy_name='greedy'):
    """
    SARSA - on-policy temporal difference algorithm
    q(s, a) = q(s, a) + alpha * (r + gamma * q(s', a') - q(s, a))

    Q-learning - similar to sarsa; the only difference is that
    sarsa employs the given policy to get the new value (a_prime),
    whereas q-learning always uses the greedy policy for that
    same task.
    q(s, a) = q(s, a) + alpha * (r + gamma * max(a')(q(s', a')) - q(s, a))

    it runs after each move

    q (dict): all q-values - format:
              state (type: list) - a hand consisting of 5 cards
              action (type: dict) - how good is each possible action {'bet': value, 'fold': value}
    s (list): old state, i.e. list of 5 cards
    a (string): old action ('bet' or 'fold')
    alpha (float): learning rate
    r (float): reward
    gamma (float): discount factor
    s_prime (list): new state, i.e. list of 5 cards
    is_sarsa (boolean): True (sarsa) or False (q-learning)
    policy_name (string): name of policy ('greedy', 'eps_greedy' or 'softmax');
                        matters only if is_sarsa is True

    """
    if is_sarsa:
        a_prime = get_action_by_policy_name(q, s_prime, policy_name)
    else:
        a_prime = greedy_policy(q[s_prime])  # use greedy policy for q-learning

    new_q_value = q[s_prime][a_prime]

    q[s][a] = q[s][a] + alpha * (r + gamma * new_q_value - q[s][a])
    return q


def sort_cards(cards):
    return tuple(sorted(cards))


def get_best_hand(cards):
    best_hand, best_score = (), 0
    for comb in helpers.combinations(cards, 5):
        val, _ = score_hand(comb, False)
        if val > best_score:
            best_hand, best_score = comb, val
    return sort_cards(best_hand)


def simulate_game(q, policy_name):
    used_cards = set()
    states_actions = {}
    hand1 = (get_random_card(used_cards), get_random_card(used_cards))
    cards_on_table = list(hand1)
    hand2 = (get_random_card(used_cards), get_random_card(used_cards))
    s_primes = []
    is_game_over = False
    for _ in range(3):  # generate flop
        cards_on_table.append(get_random_card(used_cards))

    while len(cards_on_table) < 7 and not is_game_over:
        best_hand = get_best_hand(cards_on_table)
        a = get_action_by_policy_name(q, best_hand, policy_name)

        states_actions[best_hand] = a
        if a == 'bet':
            cards_on_table.append(get_random_card(used_cards)) # s_prime
            # choose best state to add to s_primes
            s_primes.append(get_best_hand(cards_on_table))
        else:   # fold
            s_primes.append(sort_cards(cards_on_table))

    best_h1, val1, handtype1, best_h2, val2, handtype2 = score_hands(hand1, hand2, cards_on_table[2:], False)
    reward = 1
    if val1 < val2:
        reward = -1
    elif val1 == val2:
        reward = 0

    idx = 0

    for state, action in states_actions.items():
        sarsa_q_learning(q, state, action, ALPHA, reward, GAMMA, s_primes[idx], False)
        idx += 1

    # print(f'val1 {val1} val2 {val2}')
    # print([DECK_DICTIONARY[card] for card in used_cards])
    # print([DECK_DICTIONARY[card] for card in hand1], val1)
    # print(f'Best h1 {[DECK_DICTIONARY[card] for card in best_h1]} {handtype1}')
    # print([DECK_DICTIONARY[card] for card in hand2], val2)
    # print(f'Best h2 {[DECK_DICTIONARY[card] for card in best_h2]} {handtype2}')
    # print(f'Cards on table {[DECK_DICTIONARY[card] for card in cards_on_table]}')
    # print('Game over')


    return q
    '''TODO:
    1. flop
    2. turn
    3. river
    4. update state values (SARSA, Q-learning, TDL, Monte Carlo)
    5. display who won
    '''


def initialize_q():
    q = {val: {'bet': 0.0, 'fold': 0.0} for val in STATES}   # initialize q values
    return q


if __name__ == '__main__':
    ''' q values format:
    state (type: tuple) - a hand consisting of 2 or 5 cards
    action (type: dict) - how good is each possible action {'bet': value, 'fold': value}
    '''
    q = helpers.load_object('q_values.pkl')
    # q = initialize_q()
    # exit()
    policy_name = 'greedy'
    num_games = 100
    for _ in range(num_games):
        q = simulate_game(q, policy_name)
    for k, v in q.items():
        if v['bet'] != 0 or v['fold'] != 0:
            print(k, v)
    # helpers.dump_object(q, 'q_values.pkl')

