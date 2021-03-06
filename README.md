# PokerSimulation
Applied Game Theory final project, Faculty of Technical Sciences, Novi Sad, Serbia, Software Engineering Master's Studies, Fall 2020

# Overview
A simplified form of two-player poker was used in this project, namely one which allows only the actions "bet" and "fold".

In a regular 52-card deck, there are <img src="https://render.githubusercontent.com/render/math?math=52 \choose 2"> = 1326 2-card combinations, and <img src="https://render.githubusercontent.com/render/math?math=52 \choose 5"> = 2598960 5-card combinations. All in all, that's 1326 + 2598960 = 2600286 states.

Q-values format: `{state: action}` pairs; `state (type: tuple)` - a hand consisting of 2 or 5 cards, `action (type: dict)` - how good each possible action is (`{'bet': value, 'fold': value}`).

Three policies were used to update the q-values of the possible states: Q-learning with a greedy policy, SARSA with a softmax policy and SARSA with an epsilon-greedy policy. The bot was trained on 100 million hands for each of these policies, where each hand consists of a preflop, a flop, a turn and a river.

# Number of bets/folds per policy
![Chart](https://github.com/UrosOgrizovic/PokerSimulation/blob/main/Report.png)

"Aggressive" play was encouraged by the greedy policy, since the "bet" action was chosen even if the q-values for "bet" and "fold" were equal. Consequently, the same kind of play was also encouraged by the epsilon-greedy policy.

Of the three policies, SARSA softmax unsurprisingly made by far the fewest number of bets - a fact that undoubtedly stems from the definition of softmax.

# Scoring
For details about how hands were scored, see Diego Salinas's [blog post](https://towardsdatascience.com/poker-with-python-how-to-score-all-hands-in-texas-holdem-6fd750ef73d).

Win: a reward of 1 was issued if the bot had the stronger hand.

Loss: a penalty of -1 was issued if the bot had the weaker hand and if the bot hadn't folded, i.e. hadn't "realized" that the hand it had was weak. If the bot had folded, than a penalty of -0.7 was issued, thus encouraging the bot not to be overaggressive.

# Tiny scoring test
Each policy was tested on 10 million hands after training, to see how it would score.
<table align="center">
  <thead>
    <th>policy</th>
    <th>score (in millions)</th>
  </thead>
  <tbody align="center">
    <tr><td>Q-learning</td><td>1.3</td></tr>
    <tr><td>SARSA softmax</td><td>1.9</td></tr>
    <tr><td>SARSA epsilon-greedy</td><td>2.4</td></tr>
  </tbody>
</table>


# Pickle
Pickle was used to dump the q-values of a policy into a file, thus caching them for further use. Each of the resulting files is roughly 115MB in size.
