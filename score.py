

def check_four_of_a_kind(hand, suits, numbers, rnum, rlet):
    for i in numbers:
        if numbers.count(i) == 4:
            four = i
        elif numbers.count(i) == 1:
            card = i
    # Four of a Kind → 105 to 119
    score = 105 + four + card/100
    return score


def check_full_house(hand, suits, numbers, rnum, rlet):
    for i in numbers:
        if numbers.count(i) == 3:
            full = i
        elif numbers.count(i) == 2:
            p = i
    # Full House → 90 to 104
    score = 90 + full + p/100
    return score


def check_three_of_a_kind(hand, suits, numbers, rnum, rlet):
    cards = []
    for i in numbers:
        if numbers.count(i) == 3:
            three = i
        else:
            cards.append(i)
    # 3 of a Kind → 45 to 59
    score = 45 + three + max(cards) + min(cards)/1000
    return score


def check_two_pair(hand, suits, numbers, rnum, rlet):
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


def check_pair(hand, suits, numbers, rnum, rlet):
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


def check_straight(numbers, rnum):
    # a check is necessary because e.g. 8-9-10-11-12 is not a straight

    # five-high straight, i.e. baby straight
    if 11 in numbers and all(num in [11, 5, 4, 3, 2] for num in numbers):
        return 5
    # also check for straights that skip 11 (there are 3 such straights)
    elif 11 not in numbers and rnum.count(1) == 5 and\
         all(num in [14, 13, 12, 10, 9] for num in numbers) or\
         all(num in [13, 12, 10, 9, 8] for num in numbers) or\
         all(num in [12, 10, 9, 8, 7] for num in numbers) or\
         max(numbers) - min(numbers) == 4: # diff == 4 => any other straight (e.g. 8-high)
            return max(numbers)
    return 0    # no straight


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
    # get the suit for each card in the hand
    suits = [hand[i][:1] for i in range(5)]
    # get the number for each card in the hand
    numbers = [int(hand[i][1:]) for i in range(5)]
    # repetitions for each number
    rnum = [numbers.count(i) for i in numbers]
    # repetitions for each suit
    rlet = [suits.count(i) for i in suits]
    handtype = ''
    score = 0
    if 5 in rlet and all(num in [14, 13, 12, 11, 10] for num in numbers):
        handtype = 'royal flush'
        score = 135
    elif 5 in rlet and max(numbers) - min(numbers) <= 5:
        val = check_straight(numbers, rnum)
        if val > 0:
            handtype = 'straight flush'
            score = 120 + val
    elif 4 in rnum:
        handtype = 'four of a kind'
        score = check_four_of_a_kind(hand, suits, numbers, rnum, rlet)
    elif sorted(rnum) == [2, 2, 3, 3, 3]:
        handtype = 'full house'
        score = check_full_house(hand, suits, numbers, rnum, rlet)
    elif 5 in rlet:
        handtype = 'flush'
        score = 75 + max(numbers)/100
    elif rnum.count(1) == 5:
        val =  check_straight(numbers, rnum)
        if val > 0:
            handtype = 'straight'
            score = 60 + val
    elif 3 in rnum:
        handtype = 'three of a kind'
        score = check_three_of_a_kind(hand, suits, numbers, rnum, rlet)
    elif rnum.count(2) == 4:
        handtype = 'two pair'
        score = check_two_pair(hand, suits, numbers, rnum, rlet)
    elif rnum.count(2) == 2:
        handtype = 'pair'
        score = check_pair(hand, suits, numbers, rnum, rlet)
    else:
        handtype = 'high card'
        n = sorted(numbers, reverse=True)
        score = n[0] + n[1]/100 + n[2]/1000 + n[3]/10000 + n[4]/100000
    if should_print:
        print('this hand is a %s with score: %s' % (handtype, score))

    return score


if __name__ == '__main__':
    hand1 = ['H2', 'S2', 'C2', 'D2', 'H3']  # four of a kind
    hand2 = ['H3', 'H4', 'H5', 'H6', 'H7']  # straight flush
    hand3 = ['H7', 'H9', 'H2', 'H6', 'H13'] # flush
    hand4 = ['C12', 'H12', 'H3', 'D3', 'S4']    # two pair
    hand5 = ['H11', 'H12', 'H14', 'H10', 'H13'] # royal flush
    hand6 = ['H14', 'H13', 'H12', 'H11', 'H10'] # royal flush
    hand7 = ['C8', 'S5', 'D6', 'H7', 'D9']  # straight
    hand8 = ['C9', 'S14', 'D13', 'H12', 'D10']  # straight
    hand9 = ['C3', 'S2', 'D11', 'H5', 'D4']  # baby straight, i.e. high-five straight
    score_hand(hand1)
    score_hand(hand2)
    score_hand(hand3)
    score_hand(hand4)
    score_hand(hand5)
    score_hand(hand6)
    score_hand(hand7)
    score_hand(hand8)
    score_hand(hand9)
