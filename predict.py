from hand_strength import HandStrength

"""
Positions:
0 --> UTG
1 --> UTG+1
2 --> UTG+2
3 --> LJ (Lojack)
4 --> HJ (Hijack)
5 --> CO (Cutoff)
6 --> BTN (Button)
7 --> SB (SmallBlind)
8 --> BB (BigBlind)

Notation:
[C1, C2, S/O]
C1 --> Card1
C2 --> Card2
C1/C2 in "23456789TJQKA"
S/O -> If it is suited or offsuited (True: suited | False: offsuited)

Each offsuited combination weights 12 (possible combinations)
Each suited combination weigths 4 (possible combinations)
Each pocketpair combination weigths 6 (possible combinations)
"""

def PredictRangeXHand(pos, hand, board):
        p = Player(pos)
        range = p.RangeRFI()
        cards = []
        for i in board:
            cards.append(i)
        cards.append(hand[0])
        cards.append(hand[1])
        hand_strength = HandStrength(cards)
        #FLUSH POSSIBILITY
        flush_possibility = 0
        hm = {}
        for c in board:
            if c[1] not in hm:
                hm[c[1]] = 0
            hm[c[1]] += 1
        for i in hm:
            if hm[i] == 3:
                flush_possibility = 1
            if hm[i] > 3:
                flush_possibility = 2
        
        
        BeatOrTie = 0
        Lose = 0
        for possible_hand in range:
            if possible_hand[2]:
                if flush_possibility == 1:
                    if hand_strength < 50000000000:
                        Lose += 1 #(1/4 chance of flush)
                  
            cards[5] = f"{possible_hand[0]}X"
            cards[6] = f"{possible_hand[1]}Y"
            if hand_strength >= HandStrength(cards):
                if possible_hand[2]:
                    #Is suited, 4 combos
                    BeatOrTie += 4
                else:
                    if possible_hand[0] == possible_hand[1]:
                        #6 combos for pairs
                        BeatOrTie += 6
                    else:
                        #12 combos off
                        BeatOrTie += 12
            else:
                if possible_hand[2]:
                    Lose += 4
                else:
                    if possible_hand[0] == possible_hand[1]:
                        Lose += 6
                    else:
                        Lose += 12
        
        if flush_possibility == 2:
            if hand_strength < 50000000000:
                Lose += len(range)*2
            BeatOrTie//=2
        print(BeatOrTie, Lose)



class Player:
    def __init__(self, pos):
        self.pos = pos
        self.rangeList = []
    
    def Add(self, args):
        for arg in args:
            self.rangeList.append(arg)

    """
    This function returns the GTO range that
    each position should have Raising First 
    In (RFI).

    BB is not taken into consideration, they
    are already in the pot.
    """
   
    def RangeRFI(self):
        self.rangeList = []
        if self.pos >= 0:
            #Pocket pairs
            self.Add([["A", "A", False], ["K", "K", False], ["Q", "Q", False], ["J", "J", False], ["T", "T", False], ["9", "9", False], ["8", "8", False], ["7", "7", False], ["6", "6", False]])
            #offsuited combos
            self.Add([["A", "K", False], ["A", "Q", False]])
            #Suited combos
            self.Add([["A", "K", True], ["A", "Q", True], ["A", "J", True], ["A", "T", True], ["A", "9", True], ["A", "5", True], ["K", "Q", True], ["K", "J", True], ["K", "T", True], ["Q", "J", True], ["Q", "T", True], ["J", "T", True], ["T", "9", True], ["9", "8", True]])
        
        if self.pos >= 1:
            #offsuited combos
            self.Add([["A", "J", False], ["K", "Q", False]])
            #Suited combos
            self.Add([["A", "8", True], ["A", "7", True], ["A", "6", True], ["A", "4", True], ["K", "9", True], ["Q", "9", True], ["J", "9", True], ["8", "7", True]])

        if self.pos >= 2:
            #Pocket pairs
            self.Add([["5", "5", False]])
            #Suited combos
            self.Add([["A", "3", True], ["A", "2", True], ["7", "6", True]]) 

        if self.pos >= 3:
            #Pocket pairs
            self.Add([["4", "4", False]])
            #offsuited combos
            self.Add([["A", "T", False], ["K", "J", False]])
            #Suited combos
            self.Add([["6", "5", True]])

        if self.pos >= 4:
            #Pocket pairs
            self.Add([["3", "3", False], ["2", "2", False]])
            #offsuited combos
            self.Add([["Q", "J", False]])
            #Suited combos
            self.Add([["K", "8", True], ["T", "8", True], ["9", "7", True], ["5", "4", True]])
        
        if self.pos >= 5:
            #offsuited combos
            self.Add([["K", "T", False], ["Q", "T", False], ["J", "T", False]])
            #Suited combos
            self.Add([["K", "7", True], ["Q", "8", True], ["J", "8", True], ["8", "6", True], ["7", "5", True], ["6", "4", True], ["4", "3", True]])
        
        if self.pos >= 6:
            #offsuited combos
            self.Add([["K", "9", False], ["K", "8", False], ["K", "7", False], ["Q", "9", False], ["Q", "8", False], ["J", "9", False], ["J", "8", False], ["T", "9", False], ["T", "8", False], ["9", "8", False], ["9", "7", False], ["8", "7", False], ["7", "6", False]])
            #Suited combos
            self.Add([["K", "6", True], ["K", "5", True], ["K", "4", True], ["K", "3", True], ["K", "2", True], ["Q", "7", True], ["Q", "6", True], ["Q", "5", True], ["Q", "4", True], ["Q", "3", True], ["Q", "2", True], ["J", "7", True], ["J", "6", True], ["T", "7", True], ["T", "6", True], ["9", "6", True], ["8", "5", True], ["7", "4", True], ["5", "3", True], ["3", "2", True]])

        #if self.pos == 7: BLIND X BLIND to be implemented. It is another theory.     

        return self.rangeList

    """
    This function will check the odds of a hand
    against a range of a player at "pos". 

    It will calculate how often we are beating
    our opponet. Soon, RangeXRange will be 
    implemented, calculating how often our range
    of hands are beating our villain's.
    """
    



board = ["4S", "5S", "6S", "TS", "3H"]
PredictRangeXHand(1, ["7H", "8H"], board)
PredictRangeXHand(2, ["7H", "8H"], board)
PredictRangeXHand(5, ["7H", "8H"], board)
PredictRangeXHand(3, ["TH", "TD"], board)
