import numpy as np
from constants import DECK, ALPHA, GAMMA, DECK_DICTIONARY
from cards import get_random_card, combinations
import helpers
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
    a_prime = get_action_by_policy_name(q, s_prime, policy_name, is_sarsa)

    new_q_value = q[s_prime][a_prime]

    q[s][a] = round(q[s][a] + alpha * (r + gamma * new_q_value - q[s][a]), 2)
    return q


def sort_cards(cards):
    return tuple(sorted(cards))


def get_best_hand(cards):
    best_hand, best_score = (), 0
    for comb in combinations(cards, 5):
        # use cached values instead of calling score_hand()
        val, _ = hand_values_c_5[tuple(sorted(comb))]
        if val > best_score:
            best_hand, best_score = comb, val
    return sort_cards(best_hand)


def simulate_game(q, policy_name, is_sarsa, num_bets, num_folds, total_score):
    used_cards = set()
    states_actions = {} # actions for hands of first player (i.e. bot)
    hand1 = sort_cards((get_random_card(used_cards), get_random_card(used_cards)))
    cards_on_table = list(hand1)
    hand2 = sort_cards((get_random_card(used_cards), get_random_card(used_cards)))
    s_primes = []
    is_game_over = False

    # preflop
    a = get_action_by_policy_name(q, hand1, policy_name, is_sarsa)
    states_actions[hand1] = a

    if a == "bet":  # play on
        num_bets += 1

        for _ in range(3):  # generate flop
            cards_on_table.append(get_random_card(used_cards))

        # this is s_prime for s = hand1, i.e. flop is s_prime for preflop
        s_primes.append(get_best_hand(cards_on_table))

        while not is_game_over:
            best_hand = get_best_hand(cards_on_table)
            a = get_action_by_policy_name(q, best_hand, policy_name, is_sarsa)

            states_actions[best_hand] = a
            if len(cards_on_table) < 7: # if river, don't add any cards
                if a == 'bet':
                    cards_on_table.append(get_random_card(used_cards)) # s_prime
                    num_bets += 1   # for report
                else:   # fold
                    is_game_over = True
                    num_folds += 1  # for report
                # choose best state to add to s_primes
                s_primes.append(get_best_hand(cards_on_table))
            else:
                # choose best state to add to s_primes
                s_primes.append(get_best_hand(cards_on_table))
                break
    else:
        num_folds += 1
        s_primes.append(hand1)

    best_h1, val1, handtype1, best_h2, val2, handtype2 = score_hands(hand1, hand2, cards_on_table[2:], False)
    reward = 1
    if val1 < val2:
        reward = -1
        if 'fold' in states_actions.values():
            ''' penalize losses less if the player is smart and knows when to fold
            instead of playing super aggressively all the time
            '''
            reward = -0.7
    elif val1 == val2:
        reward = 0

    idx = 0
    for state, action in states_actions.items():
        sarsa_q_learning(q, state, action, ALPHA, reward, GAMMA, s_primes[idx], is_sarsa, policy_name)
        idx += 1

    print(f'Used cards {[DECK_DICTIONARY[card] for card in used_cards]}')
    print(f'h1 and value of h1 {[DECK_DICTIONARY[card] for card in hand1], val1}')
    print(f'Best h1 {[DECK_DICTIONARY[card] for card in best_h1]} {handtype1}')
    print(f'h2 and value of h2 {[DECK_DICTIONARY[card] for card in hand2], val2}')
    print(f'Best h2 {[DECK_DICTIONARY[card] for card in best_h2]} {handtype2}')
    print(f'Cards on table {[DECK_DICTIONARY[card] for card in cards_on_table]}')
    print(f'Reward {reward}')

    for state, action in states_actions.items():
        print([DECK_DICTIONARY[card] for card in state], action)
    print('Game over')

    return q, num_bets, num_folds, total_score + reward


def get_num_changed_states(q):
    changed = 0
    for k, v in q.items():
        if v['bet'] != 0 or v['fold'] != 0:
            changed += 1
    return changed


if __name__ == '__main__':
    ''' q values format:
    state (type: tuple) - a hand consisting of 2 or 5 cards
    action (type: dict) - how good is each possible action {'bet': value, 'fold': value}
    (52 choose 2) = 1326 - number of 2-card combinations
    (52 choose 5) = 2598960 - number of 5-card combinations
    There are 1326 + 2598960 = 2600286 possible states.
    Q-learning:
        Number of games simulated: 10^8
        Number of states changed: 2592084
        Number of bets: 45321468
        Number of folds: 93473472
        Total score: 1344995.70
    SARSA (softmax policy):
        Number of games simulated: 10^8
        Number of states changed: 2180564
        Number of bets: 17153597
        Number of folds: 99616300
        Total score: 1911379.7
    SARSA (eps_greedy policy):
        Number of games simulated: 10^8
        Number of states changed: 2598760
        Number of bets: 80094992
        Number of folds: 89127500
        Total score: 2374996.5
    '''
    _, _, _, hand_values_c_5 = helpers.initialize_files()
    is_sarsa = True
    policy_name = 'eps_greedy'
    q_values_path = helpers.get_q_values_path(is_sarsa, policy_name)
    q = helpers.get_q_values_object(q_values_path)
    # q = helpers.initialize_q()

    num_bets, num_folds, total_score = 0, 0, 0
    num_games = 1
    for i in range(num_games):
        if i > 0.5 * num_games:
            ALPHA *= 0.5    # reduce learning rate
        # if i % 10**6 == 0:
        #     print(f'Game index {i}')
        q, num_bets, num_folds, total_score = simulate_game(q, policy_name,
                                                            is_sarsa, num_bets,
                                                            num_folds, total_score)

    changed = get_num_changed_states(q)
    print(f'Policy name: {policy_name}')
    print(f'Num states changed: {changed}')
    print(f'Num bets made: {num_bets}')
    print(f'Num folds made: {num_folds}')
    print(f'Total score: {round(total_score, 2)}')
    # helpers.dump_object(q, q_values_path)
