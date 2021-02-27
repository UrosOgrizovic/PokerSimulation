import helpers

"""2 - 14 - hearts
   17 - 29 - spades
   32 - 44 - clubs
   47 - 59 - diamonds
   e.g. 2 = 2 of hearts, ..., 9 = 9H, 10 = 10H, 11 = 12H, 12 = 13H, 13 - 14H, 14 - ace of hearts (AH)
   17 = 2 of spades etc.

   The deck is set up in this way so that mod(15) can be used effectively.
"""
DECK = list(range(2, 15)) + list(range(17, 30)) +\
           list(range(32, 45)) + list(range(47, 60))
# for printing
DECK_DICTIONARY = {2: '2H', 3: '3H', 4: '4H', 5: '5H', 6: '6H', 7: '7H', 8: '8H', 9: '9H', 10: '10H',
                   11: '12H', 12: '13H', 13: '14H', 14: 'AH',
                   17: '2S', 18: '3S', 19: '4S', 20: '5S', 21: '6S', 22: '7S', 23: '8S', 24: '9S',
                   25: '10S', 26: '12S', 27: '13S', 28: '14S', 29: 'AS',
                   32: '2C', 33: '3C', 34: '4C', 35: '5C', 36: '6C', 37: '7C', 38: '8C', 39: '9C',
                   40: '10C', 41: '12C', 42: '13C', 43: '14C', 44: 'AC',
                   47: '2D', 48: '3D', 49: '4D', 50: '5D', 51: '6D', 52: '7D', 53: '8D', 54: '9D',
                   55: '10D', 56: '12D', 57: '13D', 58: '14D', 59: 'AD',}

c_2 = helpers.load_object('c_2.pkl')
c_5 = helpers.load_object('c_5.pkl')
hand_values_c_5 = helpers.load_object('hand_values_c_5.pkl')   # {hand: (score, handtype)}

ALPHA = 0.6
GAMMA = 0.4

if __name__ == '__main__':
   print(type(c_5))
   for val in c_5:
      print(val, type(val))
      break