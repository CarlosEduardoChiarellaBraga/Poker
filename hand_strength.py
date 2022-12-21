def straight_flush(cards):
    #At least 5 must have the same suit:
    suits = {}
    str_values = '__23456789TJQKA'
    val = -1
    for i in range(0, len(cards)):
        if cards[i][1] not in suits:
            suits[cards[i][1]] = 1
        else:
            suits[cards[i][1]] +=1
    suit = ""
    for k in suits:
        if suits[k] >= 5:
            suit = k
    if suit == "":
        return -1

    #Check the values of the cards that have the suit required & store them sorted at possible_s_f
    possible_s_f = []
    for card in cards:
        if card[1]==suit:
            possible_s_f.append(card[0])
    possible_s_f.sort(key=lambda x: str_values.index(x))
    print(possible_s_f)
    val = -1
    #Check if it is straight
    for i in range(len(possible_s_f) - 4):
        possibility = possible_s_f[i:i+5]
        if (str_values.index(possibility[-1][0]) - str_values.index(possibility[0][0])) == 4: #Check if it is a straight
            #Adding the value if it is higher than the current
            if str_values.index(possibility[0][0])>val: 
                val = str_values.index(possibility[0][0])
    #Check special case ("A, 2, 3, 4 ,5")
    if possible_s_f[-1] == "A":
        if possible_s_f[0] == "2" and possible_s_f[1] == "3" and possible_s_f[2] == "4" and possible_s_f[3] == "5":
            if val<1:
                val = 1
    val += 800
    val = val * 100000000
    return val
  
  
  
  
