def HandStrength(cards):
    val = 0
    str_values = '__23456789TJQKA'

    def straight_flush():
        #At least 5 must have the same suit:
        suits = {}
        val_ = -1
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
        val_ = -1
        #Check if it is straight
        for i in range(len(possible_s_f) - 4):
            possibility = possible_s_f[i:i+5]
            if (str_values.index(possibility[-1][0]) - str_values.index(possibility[0][0])) == 4: #Check if it is a straight
                #Adding the value if it is higher than the current
                if str_values.index(possibility[0][0])>val_: 
                    val_ = str_values.index(possibility[0][0])
        #Check special case ("A, 2, 3, 4 ,5")
        if possible_s_f[-1] == "A":
            if "2" in possible_s_f and "3" in possible_s_f and "4" in possible_s_f and "5" in possible_s_f:
                if val_<1:
                    val_ = 1
        if val_ > 0:
            val_ += 800
            val_ = val_ * 100000000
        return val_

    def flush():
        #At least 5 must have the same suit:
        suits = {}
        val_ = -1
        for i in range(0, len(cards)):
            if cards[i][1] not in suits:
                suits[cards[i][1]] = 1
            else:
                suits[cards[i][1]] +=1
        suit = ""
        for k in suits:
            if suits[k] >= 5:
                suit = k
        #not a flush:
        if suit == "":
            return val_
        #is a flush:
        cards_values = []
        for card in cards:
            if card[1]==suit:
                cards_values.append(card[0])
        cards_values.sort(key=lambda x: str_values.index(x))
        val_ = 5
        cont_kickers = 0
        for i in range(len(cards_values)-1, -1, -1):
            val_*=100
            val_ += str_values.index(cards_values[i])
            cont_kickers += 1
            if cont_kickers == 5:
                break
        return val_

    def straight():
        possible_straight = []
        for card in cards:
            if card[0] not in possible_straight: #(check if the cards are repeated)
                possible_straight.append(card[0])
            
        possible_straight.sort(key=lambda x: str_values.index(x))
        val_ = -1
        #Check if it is straight
        for i in range(len(possible_straight) - 4):
            possibility = possible_straight[i:i+5]
            if (str_values.index(possibility[-1][0]) - str_values.index(possibility[0][0])) == 4: #Check if it is a straight
                #Adding the value if it is higher than the current
                if str_values.index(possibility[0][0])>val_: 
                    val_ = str_values.index(possibility[0][0])
        #Check special case ("A, 2, 3, 4 ,5")
        if possible_straight[-1] == "A":
            if "2" in possible_straight and "3" in possible_straight and "4" in possible_straight and "5" in possible_straight:
                if val_<1:
                    val_ = 1
        if val_ > 0:
            val_ += 400
            val_ = val_ * 100000000
        return val_

    #Check if hand is: High card, Pair, Two pair, Three of a kind, Full house or Four of a kind
    def count_repeated():    
        cards_rep = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, 'T': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0}
        highest_rep =  [-1, ""]
        second_highest = [-2, ""]
        val_ = -1
        for i in range(0, len(cards)):
            cards_rep[cards[i][0]] += 1
            
        for key in cards_rep:
            #If the current card repeats more than the highest repeated, it is now the highest. The previous one will be the second highest
            if cards_rep[key] > highest_rep[0]:
                second_highest[0] = highest_rep[0]
                second_highest[1] = highest_rep[1]
                highest_rep[0] = cards_rep[key]
                highest_rep[1] = key
            #Else if it is higher than the second higher only, it will be replaced.
            elif cards_rep[key] > second_highest[0]:
                second_highest[0] = cards_rep[key]
                second_highest[1] = key

        #highest_rep: the card with the greatest repetition number, second_highest: the card with the second greatest repetition number
        #Observation: if highest_rep[0] == second_highest[0], the highest_rep[1] will be greater than the second_highest[1]
        #highest_rep -> 1 = High card
        #highest_rep -> 2 = Pair or Two pair (in case of three pairs, it is guaranteed to the 2 biggest be at the highest_rep and second_higher)
        #highest_rep -> 3 = Three of a kind or Full House
        #highest_rep -> 4 = Four of a kind

        if highest_rep[0] == 1:
            #High card: val_ = (0){highcard1}{highcard2}{highcard3}{highcard4}{highcard5}
            val_ = 0
            kicker = ""
            cont_kickers = 0
            #Find the 5 highest cards:
            for i in cards_rep:
                if cards_rep[i] > 0:
                    kicker = i
                    val_ += str_values.index(kicker)
                    cont_kickers+=1
                    if cont_kickers==5:
                        break
                    else: #Prepare to receive the next value
                        val_ *= 100
            return val_ #1{pair}{kicker1}{kicker2}{kicker3}00

        if highest_rep[0] == 2:
            if second_highest[0] == 2:
                #Two pair: val_ = 2{pair1}{pair2}{kicker}0000
                #Define the value of the two pairs
                val_ = 200
                val_ += str_values.index(highest_rep[1])
                val_ *= 100
                val_ += str_values.index(second_highest[1])
                kicker = ""
                #Find the kicker
                for i in cards_rep:
                    if i != highest_rep[1] and i != second_highest[1] and cards_rep[i] > 0:
                        kicker = i
                        break
                #Add the kicker value and return it
                val_ *= 100
                val_ += str_values.index(kicker)
                val_ *= 10000
                return val_ #2{pair1}{pair2}{kicker}0000
          
            else:
                #Pair: val_ = 1{pair}{kicker1}{kicker2}{kicker3}00
                #Define the value of the pair
                val_ = 100
                val_ += str_values.index(highest_rep[1])
                val_ *= 100
                kicker = ""
                cont_kickers = 0
                #Find the 3 kickers:
                for i in cards_rep:
                    if i != highest_rep[1] and cards_rep[i] > 0:
                        kicker = i
                        val_ += str_values.index(kicker)
                        val_ *= 100
                        cont_kickers+=1
                    if cont_kickers==3:
                        break                                
                return val_ #1{pair}{kicker1}{kicker2}{kicker3}00

        if highest_rep[0] == 3:
            if second_highest[0] >= 2:
                #Full house: val_ = 6{three_cards}{pair}000000
                #Define the value of the full house
                val_ = 600
                val_ += str_values.index(highest_rep[1])
                val_ *= 100
                val_ += str_values.index(second_highest[1])  
                val_ *= 1000000
                return val_ #6{three_cards}{pair}000000
            
            else:
                #Three of a kind: val_ = 3{three_cards}{kicker1}{kicker2}0000
                #Define the value of the three of a kind
                val_ = 300
                val_ += str_values.index(highest_rep[1])
                val_ *= 100
                kicker = ""
                cont_kickers = 0
                #Find the 2 kickers:
                for i in cards_rep:
                    if i != highest_rep[1] and cards_rep[i] > 0:
                        kicker = i
                        val_ += str_values.index(kicker)
                        val_ *= 100
                        cont_kickers+=1
                    if cont_kickers==2:
                        break       
                val_ *= 100
                return val_ #3{three_cards}{kicker1}{kicker2}0000  

        if highest_rep[0] == 4:
            #Four of a kind: val_ = 7{four_cards}{kicker}000000
            #Define the value of the four of a kind
            val_ = 700
            val_ += str_values.index(highest_rep[1])
            val_ *= 100
            kicker = ""
            #Find the kicker:
            for i in cards_rep:
                if i != highest_rep[1] and cards_rep[i] > 0:
                    kicker = i
                    val_ += str_values.index(kicker)
                    break   

            val_ *= 1000000
            return val_ #7{four_cards}{kicker}000000

        return

    #check if it is straight_flush
    val_temp = straight_flush()
    if val < val_temp: val = val_temp

    #check for: pair, two pair, three of a kind, full house, four of a kind
    val_temp = count_repeated()
    if val < val_temp: val = val_temp 
    

    val_temp = flush()
    if val < val_temp: val = val_temp

    return val

cards = ["4S", "4S", "4S", "4S", "JS", "TH", "3H"]
print(HandStrength(cards))
