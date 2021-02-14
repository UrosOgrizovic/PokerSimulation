

def check_four_of_a_kind(numbers):
    for num in numbers:
        if numbers.count(num) == 4:
            # Four of a Kind → 105 to 119
            return 105 + num


def check_full_house(numbers):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    # Full House → 90 to 104
    score = 90 + full + p/100
    return score


def check_three_of_a_kind(numbers):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else:
            cards.append(i)
    # 3 of a Kind → 45 to 59
    score = 45 + three + max(cards) + min(cards)/1000
    return score


def check_two_pair(numbers):
    pairs = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pairs.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards, reverse=True)
    # Two Pair → 30 to 44
    score = 30 + max(pairs) + min(pairs)/100 + cards[0]/1000
    return score


def check_pair(numbers):
    pair = []
    cards = []
    for i in numbers:
        if numbers.count(i) == 2:
            pair.append(i)
        elif numbers.count(i) == 1:
            cards.append(i)
            cards = sorted(cards, reverse=True)
    # Pair → 15 to 29
    score = 15 + pair[0] + cards[0]/100 + cards[1]/1000 + cards[2]/10000
    return score


def get_suits(hand):
    suits = []
    for card in hand:
        if card < 15:   # hearts
            suits.append(0)
        elif card < 30: # spades
            suits.append(1)
        elif card < 45: # clubs
            suits.append(2)
        else:   # diamonds
            suits.append(3)
    return suits


def score_hand(hand, should_print=True):
    """Scoring explained:
        High card → 0 to 14
        Pair → 15 to 29
        Two Pair → 30 to 44
        3 of a Kind → 45 to 59
        Straight → 60 to 74
        Flush → 75 to 89
        Full House → 90 to 104
        Four of a Kind → 105 to 119
        Straight Flush → 120 to 134
        Royal Flush → 135
    """
    numbers = [card % 15 for card in hand]
    # repetitions for each number
    reps_num = [numbers.count(num) for num in numbers]

    suits = get_suits(hand)
    # repetitions for each suit
    reps_suit = [suits.count(suit) for suit in suits]
    handtype = ''
    score = 0
    if 5 in reps_suit and all(num in range(10, 15) for num in numbers):
        handtype = 'royal flush'
        score = 135
    elif 5 in reps_suit and reps_num.count(1) == 5 and max(numbers) - min(numbers) == 4:
        handtype = 'straight flush'
        score = 120 + max(numbers)
    elif 5 in reps_suit and all(num in [14, 2, 3, 4, 5] for num in numbers):    # baby straight
        handtype = 'straight flush'
        score = 120 + 5
    elif 4 in reps_num:
        handtype = 'four of a kind'
        score = check_four_of_a_kind(numbers)
    elif sorted(reps_num) == [2, 2, 3, 3, 3]:
        handtype = 'full house'
        score = check_full_house(numbers)
    elif 5 in reps_suit:
        handtype = 'flush'
        score = 75 + max(numbers)/100
    elif reps_num.count(1) == 5 and max(numbers) - min(numbers) == 4:
        handtype = 'straight'
        score = 60 + max(numbers)
    elif all(num in [14, 2, 3, 4, 5] for num in numbers):    # baby straight
        handtype = 'straight'
        score = 60 + 5
    elif 3 in reps_num:
        handtype = 'three of a kind'
        score = check_three_of_a_kind(numbers)
    elif reps_num.count(2) == 4:
        handtype = 'two pair'
        score = check_two_pair(numbers)
    elif reps_num.count(2) == 2:
        handtype = 'pair'
        score = check_pair(numbers)
    else:
        handtype = 'high card'
        n = sorted(numbers, reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
    score = round(score, 2)
    if should_print:
        print('this hand is a %s with score: %s' % (handtype, score))

    return score


if __name__ == '__main__':
    hand1 = [2, 17, 32, 47, 3]  # four of a kind (four twos)
    hand2 = list(range(3, 8))  # straight flush
    hand3 = [7, 9, 2, 6, 13] # flush
    hand4 = [41, 11, 3, 48, 19] # two pair  ['C12', 'H12', 'H3', 'D3', 'S4']
    hand5 = [11, 12, 14, 10, 13] # royal flush
    hand6 = [14, 13, 12, 11, 10] # royal flush
    hand7 = [38, 20, 51, 7, 54]  # straight ['C8', 'S5', 'D6', 'H7', 'D9']
    hand8 = [39, 28, 57, 11, 55]  # straight    ['C9', 'S14', 'D13', 'H12', 'D10']
    hand9 = [33, 17, 59, 5, 49]  # baby straight, i.e. high-five straight ['C3', 'S2', 'D11', 'H5', 'D4']
    hand10 = [7, 22, 37, 48, 3] # full house ['H7', 'S7', 'C7', 'D3', 'H3']

    hand11 = [13, 28, 43, 59, 10]   # three of a kind ['HK', 'SK', 'CK', 'DA', 'H10']
    hand12 = [13, 28, 43, 57, 10]   # three of a kind ['HK', 'SK', 'CK', 'D13', 'H10']
    # hand12 score is lower than hand11 score because of the high card (A vs 13)

    hand13 = [8, 23, 36, 51, 3] # two pair ['H8', 'S8', 'C6', 'D6', 'H3']
    hand14 = [7, 22, 34, 56, 3] # pair ['H7', 'S7', 'C4', 'D12', 'H3']
    hand15 = [14, 17, 33, 51, 55]   # high card ['HA', 'S2', 'C3', 'D6', 'D10']
    hand16 = [7, 17, 33, 51, 41]   # high card ['H7', 'S2', 'C3', 'D6', 'D12']
    
    score_hand(hand1)
    score_hand(hand2)
    score_hand(hand3)
    score_hand(hand4)
    score_hand(hand5)
    score_hand(hand6)
    score_hand(hand7)
    score_hand(hand8)
    score_hand(hand9)
    score_hand(hand10)
    score_hand(hand11)
    score_hand(hand12)
    score_hand(hand13)
    score_hand(hand14)
    score_hand(hand15)
    score_hand(hand16)
