# Documentation of hand strength storage:
The hands will be stored in a list
The first index of the list will represent what type of hand it is, in the order of their strength:

0->high card, 1->pair, 2->two pair, 3->three of a kind, 4->straight, 5->flush, 6->full house, 7->quads, 8->straight flush

For each one of these values, a certain amount of values will follow them, due to tiebreaks. 

### For idx[0] == 0:

    Five values will follow, in descending order. The first player that has a card bigger than the other wins.
    
    Ex: [0, 14, 13, 10, 8, 7]  (High-Card: A, Kicker: K...) (The hand is: A K T 8 7)

### For idx[0] == 1:

    Four values will follow. The first will be the value of the pair. The remaining 3 represent the others cards.
    
    Ex: [1, 6, 13, 12, 9] (Pair: Sixes, Kicker: K...) (The hand is: 6 6 K Q 9)

### For idx[0] == 2:

    Three values will follow. The first and the second will be the values of the pairs, in descending order. The remaining represent the other card.
    
    Ex: [2, 8, 7, 11] (Two pair: Eights and Sevens, Kicker: J) (The hand is: 8 8 7 7 J)
    Ex: [2, 7, 5, 3] (Two pair: Sevens and Fives, Kicker: 3) (The hand is: 7 7 5 5 3)

### For idx[0] == 3:

    Two values will follow. The first will be the value of the three of a kind. The remaining two represent the others cards, in descending order.
    
    Ex: [3, 8, 11, 7] (Three of a kind: Eights, Kicker: J, Last Kicker: 7) (The hand is: 8 8 8 J 7)

### For idx[0] == 4:

    One value will follow. That is the starting point of the straight
    
    Ex: [4, 8] (Straight: 8 to Q) (The hand is: 8 9 T J Q)
    
### For idx[0] == 5:

    Five values will follow, in descending order. The first player that has a card bigger than the other wins.
    
    Ex: [5, 14, 13, 10, 8, 7]  (Flush) (The hand is: A K T 8 7 (suited)). Note that the difference from this example to the example of the idx[0] == 0 is only the first value.
