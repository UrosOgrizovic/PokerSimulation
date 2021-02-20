import numpy as np
from random import random, randint


def greedy_policy(q):
    """
    choose the best action

    q (dict): {'bet': val1, 'fold': val2}
    Returns:
        string: best action
    """
    return 'bet' if q['bet'] >= q['fold'] else 'fold'


def eps_greedy_policy(q, eps=0.1):
    """
    choose a random action with a probability of eps,
    otherwise choose best action, i.e. greedy

    q (dict): {'bet': val1, 'fold': val2}
    eps (float): exploration/exploitation threshold
    Returns:
        string: random/best action
    """
    if random() < eps:
        # choose random action
        if randint(0, len(q)) == 0:
            return 'bet'
        return 'fold'
    else:
        return greedy_policy(q)


def softmax_policy(q):
    """
    the probability of choosing an action is proportional to its q-value

    q (dict): e.g. {'bet': val1, 'fold': val2}
    Returns:
        string: chosen action
    """
    s = np.exp(q['bet']) + np.exp(q['fold'])

    probs_actions = {'bet': np.exp(q['bet'] / s), 'fold': np.exp(q['fold'] / s)}

    rand_prob = random()

    best_action = max(probs_actions)
    worst_action = min(probs_actions)

    return best_action if probs_actions[best_action] >= rand_prob else worst_action


def get_action_by_policy_name(q_values, state, policy_name):
    """
    get action for q value and a specific policy

    q_values (dict): all q_values
    state (set): current hand of length 5
    policy_name (string): the name of the policy to be adopted
    """
    if policy_name == 'greedy':
        action = greedy_policy(q_values[state])
    elif policy_name == 'eps_greedy':
        action = eps_greedy_policy(q_values[state])
    elif policy_name == 'softmax':
        action = softmax_policy(q_values[state])
    else:
        raise ValueError("Invalid policy name")
    return action
