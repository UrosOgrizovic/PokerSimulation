# PokerSimulation
Applied Game Theory final project, Faculty of Technical Sciences, Novi Sad, Serbia, Software Engineering Master's Studies, Fall 2020

# Overview
A simplified form of poker was used in this project, namely one which recognizes only the actions "bet" and "fold".

In a regular 52-card deck, there are <img src="https://render.githubusercontent.com/render/math?math=52 \choose 2"> = 1326 2-card combinations, and <img src="https://render.githubusercontent.com/render/math?math=52 \choose 5"> = 2598960 5-card combinations. All in all, that's 1326 + 2598960 = 2600286 states.

Q-values format: `{state: action}` pairs; `state (type: tuple)` - a hand consisting of 2 or 5 cards, `action (type: dict)` - how good each possible action is (`{'bet': value, 'fold': value}`).

Three policies/algorithms were used to update the q-values of the possible states: Q-learning with a greedy policy, SARSA with a softmax policy and SARSA with an epsilon-greedy policy. The bot was trained on 10 million hands for each of these algorithms, where each hand consists of a flop, a turn and a river.

# Number of bets/folds per training algorithm
![Chart](https://github.com/UrosOgrizovic/PokerSimulation/blob/main/Report.png)

"Aggressive" play was encouraged by the greedy policy, since the "bet" action was chosen even if the q-values for "bet" and "fold" were equal. Consequently, the same kind of play was also encouraged by the epsilon-greedy policy.

Of the three policies, SARSA softmax unsurprisingly made by far the fewest number of bets - a fact that undoubtedly stems from the definition of softmax.

# Scoring hands
Diego Salinas's [blog post](https://towardsdatascience.com/poker-with-python-how-to-score-all-hands-in-texas-holdem-6fd750ef73d).

# Pickle
Pickle was used to dump the q-values of an algorithm into a file, thus caching them for further use. Each of the resulting files is roughly 115MB in size.
