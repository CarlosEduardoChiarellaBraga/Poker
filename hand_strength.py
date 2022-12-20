def straight_flush(cards):
    #Sorting the cards
    values = [card[:-1] for card in cards]
    values.sort(key=lambda x: '23456789TJQKA'.index(x))
    val = -1
    while len(cards)>0:
        card = cards[0]
        idx = values.index(card[0])
        values[idx]+=(card[1])
        cards.pop(0)
    #Check if it is straight flush
    for i in range(len(values) - 4):
        straight_flush = values[i:i+5]
        if ('23456789TJQKA'.index(straight_flush[-1][0]) - '23456789TJQKA'.index(straight_flush[0][0])) == 4: #Check if it is a straight
            if all(card[-1] == straight_flush[0][-1] for card in straight_flush): #Check if it is the same suit
                #Adding the value if it is higher than the current
                if 1525+'23456789TJQKA'.index(straight_flush[-1][0])>val: 
                    val = 1525+'23456789TJQKA'.index(straight_flush[0][0])
    #Check special case ("A, 2, 3, 4 ,5")
    if values[-1][0] == "A":
        if values[0][0] == "2":
            straight_flush = values[0:4]
            straight_flush.append(values[-1])
            if '23456789TJQKA'.index(straight_flush[3][0]) - '23456789TJQKA'.index(values[0][0]) == 3:
                if all(card[-1] == straight_flush[0][-1] for card in straight_flush):
                    if val<1525:
                        val = 1524
    return val
