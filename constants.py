import helpers

# total number of 5-card combinations from a 52-card deck
TOTAL_NUM_COMBINATIONS = 2598960

NUM_PLAYERS = 2

"""2 - 14 - hearts
   17 - 29 - spades
   32 - 44 - clubs
   47 - 59 - diamonds
   e.g. 2 = 2 of hearts, ..., 9 = 9H, 10 = 10H, 11 = 12H, 12 = 13H, 13 - 14H, 14 - ace of hearts (AH)
   17 = 2 of spades etc.
"""
DECK = list(range(2, 15)) + list(range(17, 30)) +\
           list(range(32, 45)) + list(range(47, 60))

c_5 = helpers.load_object('c_5.pkl')
hand_values_c_5 = helpers.load_object('hand_values_c_5.pkl')
all_hands_df = helpers.load_object('all_hands_df.pkl')