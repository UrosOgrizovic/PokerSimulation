import helpers

# total number of 5-card combinations from a 52-card deck
TOTAL_NUM_COMBINATIONS = 2598960

NUM_PLAYERS = 2

deck = helpers.load_object('deck.pkl')
c_5 = helpers.load_object('c_5.pkl')
hand_values_c_5 = helpers.load_object('hand_values_c_5.pkl')
all_hands_df = helpers.load_object('all_hands_df.pkl')