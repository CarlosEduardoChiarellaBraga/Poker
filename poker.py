import random
import time
from hand_strength import HandStrength
from operator import itemgetter

#Setting game variables:
num_players = 9 #Players at the table

class Player:
    inTheHand = True
    inTheGame = True
    isBTN = False
    lastAction = False
    isAllIn = False
    starting_chips = 5000
    cur_bet = 0
    blinds = 30 #(BB)
    min_bet = 0 #Keep track of the min bet
    pot = 0
    hand_strength = 0

    def __init__(self, table_seat, cards):
        self.chips = Player.starting_chips
        self.table_seat = table_seat
        self.cards = cards 

    def RaiseBlind(self, bet):
        if self.chips>=bet:
            Player.pot += bet - self.cur_bet
            self.chips -= bet
            self.cur_bet = bet
            Player.min_bet = bet
        else:
            print("All In")
            self.AllIn()

    def Call(self):
        if self.chips < Player.min_bet:
            Player.pot += self.chips
            self.cur_bet += self.chips
            self.chips = 0
            print(f"Player {self.table_seat} called for {self.cur_bet}, with {self.chips} remaining chips")
            return 1
        else:
            Player.pot += Player.min_bet - self.cur_bet
            self.chips -= Player.min_bet - self.cur_bet
            self.cur_bet = Player.min_bet
            return 1
    
    def Check(self):
        print("Check")
        if self.cur_bet == Player.min_bet:
            return 1
        elif self.chips == 0:
            return 1
        return -1
         
    def Raise(self):
        bet = int(input(f"Raise to: "))
        if self.chips>=bet:
            if bet >= Player.min_bet + Player.blinds:
                Player.pot += bet - self.cur_bet
                self.chips -= bet
                self.cur_bet = bet
                Player.min_bet = bet
            else:
                print("Small increase. Call/Check")
                self.Call()
        else:
            print("All In")
            self.AllIn()

    def AllIn(self):
        self.isAllIn = True
        self.cur_bet+=self.chips
        Player.pot += self.chips
        self.chips = 0
        if Player.min_bet < self.cur_bet:
            Player.min_bet = self.cur_bet
            
            
        print(f"Player {self.table_seat} is all in for {self.cur_bet}. Min bet now is {Player.min_bet}, player has {self.chips} chips left")
        return 1

    def Fold(self):
        self.inTheHand = False

    def PrintCards(self):
        s = f"[{self.cards[0]} {self.cards[1]}]"
        for i in range(2, len(self.cards)):
            s+=f" {self.cards[i]}"
        print(s)


def PrintBlanks(n):
    for i in range(0, n):
        print("")

def Hand(table):
    def Winner():
        #Classify the people on the table, from first to last (for multi-pots hands)
        if PlayersLeft() == 1:
            for i in range(0, len(table)):
                if table[i].inTheHand:
                    return [[table[i].hand_strength, i]]
        winners = []
        for i in range(0, len(table)):
            if table[i].inTheHand:
                table[i].hand_strength = HandStrength(table[i].cards)
                winners.append([table[i].hand_strength, i])
                winners.sort(key=itemgetter(0), reverse=True)
        print(winners)
        return winners

    def AwardPot():
        w = Winner()
        if len(w) == 1: 
            table[w[0][1]].chips += Player.pot
            Player.pot = 0
        else: #Side pots not implemented yet
            table[w[0][1]].chips += Player.pot 
            Player.pot = 0
        
    def PrintTableSituation():
        for player in table:
            print(f"Player {player.table_seat}: Chips = {player.chips}")
        print(f"Total pot: {Player.pot}")

    def PlayersLeft():
        left = 0
        for i in range(0, len(table)):
            if table[i].inTheHand:
                left+=1
        return left

    def RotateBTN():
        btn = 999
        for i in range(0, len(table)):
            if table[i].isBTN == True:
                table[i].isBTN = False
                btn = i
            if i>btn:
                if table[i].inTheGame == True:
                    table[i].isBTN = True
                    return 0
        for i in range(0, len(table)):
            if table[i].inTheGame == True:
                table[i].isBTN = True
                return 0
        return -1

    def ResetLastAction():
        for player in table:
            player.lastAction = False

    def ResetCurBet():
        for player in table:
            player.cur_bet = 0

    def ResetAllIn():
        for player in table:
            player.isAllIn = False

    def BettingMenu(player): 
        if player.isAllIn:
            return 
        min_before = Player.min_bet
        PrintBlanks(10)
        print(f"Player{player.table_seat}'s turn")
        print(f"Pot: {Player.pot}")
        player.PrintCards()
        print(f"You have: {player.chips} chips.")
        print(f"Min-bet is {Player.min_bet} chips.")
        print(f"Your current bet: {player.cur_bet} chips.")
        choice = ""
        if player.cur_bet == Player.min_bet:
            while choice!="A" and choice!="C" and choice!="R":
                print("[A]: All in")
                print("[C]: Check")
                print("[R]: Raise")
                choice = input("Your decision: ")
                if choice == "A": player.AllIn()
                if choice == "C": player.Check()
                if choice == "R": player.Raise()
                       
        elif player.cur_bet + player.chips <= Player.min_bet:
            while choice!="A" and choice!="F":
                print("[A]: All in")
                print("[F]: Fold")
                choice = input("Your decision: ")
                if choice == "A": player.AllIn()
                if choice == "F": player.Fold()

        else:
            while choice!="A" and choice!="C" and choice!="R" and choice!="F":
                print("[A]: All in")
                print("[C]: Call")
                print("[R]: Raise")
                print("[F]: Fold")
                choice = input("Your decision: ")
                if choice == "A": player.AllIn()
                if choice == "C": player.Call()
                if choice == "R": player.Raise()
                if choice == "F": player.Fold()
        if Player.min_bet > min_before:
            #Check the last action
            last_to_play = player.table_seat-1
            while(table[last_to_play].inTheHand==False):
                last_to_play -= 1
            print(f"Last to play is {last_to_play}")
            ResetLastAction()
            table[last_to_play].lastAction = True

    def Deal():
        for person in table:
            if person.inTheGame:
                person.inTheHand = True
                card = random.choice(deck)
                deck.remove(card)
                person.cards.append(card)
                card = random.choice(deck)
                deck.remove(card)
                person.cards.append(card)
       
    def TakeCards():
        for person in table:
            person.cards = []
        return

    def PreFlopBets():
        for i in range(0, len(table)):
            if table[i].isBTN:
                sb = i+1
                if sb>=len(table): sb-=len(table)
                bb = i+2
                if bb>=len(table): bb-=len(table)
                first = i+3
                if first>=len(table): first-=len(table)

        Player.min_bet = 0
        table[sb].RaiseBlind(Player.blinds/2)
        table[bb].RaiseBlind(Player.blinds)
        Player.min_bet = Player.blinds
        table[bb].lastAction = True

        cur_player = first
        while(1):
            if cur_player>=len(table): cur_player-=len(table)    

            if table[cur_player].inTheHand and table[cur_player].inTheGame:
                if PlayersLeft()!=1: BettingMenu(table[cur_player])
                else:
                    return True
            if table[cur_player].lastAction: break #If the lastAction does raise, lastAction--> table[cur_player-1]
            cur_player+=1

        if PlayersLeft() == 1:
            return True #is finished
        return False

    def Flop():
        card1 = random.choice(deck)
        deck.remove(card1)
        card2 = random.choice(deck)
        deck.remove(card2)
        card3 = random.choice(deck)
        deck.remove(card3)
        for player in table:
            player.cards.append(card1)
            player.cards.append(card2)
            player.cards.append(card3)
        print(f"Flop: {card1} {card2} {card3}")

    def RiverOrTurn(turn=False):
        card = random.choice(deck)
        deck.remove(card)
        for player in table:
            player.cards.append(card)
        if turn: print(f"Turn: {card}")
        else: print(f"River: {card}")

    def BettingRound():
        ResetLastAction()
        ResetCurBet()
        for i in range(0, len(table)):
            if table[i].isBTN:
                table[i].lastAction = True
                cur_player = i+1
                break

        Player.min_bet = 0
        
        while(1):
            if cur_player>=len(table): cur_player-=len(table)          
            if table[cur_player].inTheHand and table[cur_player].inTheGame: BettingMenu(table[cur_player])

            if table[cur_player].lastAction: break #If the lastAction does raise, lastAction--> table[cur_player-1]
            cur_player+=1
        if PlayersLeft() == 1:
            return True #is finished
        return False

    def NextHand():
        RotateBTN()
        ResetLastAction()
        TakeCards()
        ResetAllIn()
        ResetCurBet()
        

    deck = ["2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "TA", "JA", "QA", "KA", "AA",
        "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "TB", "JB", "QB", "KB", "AB",
        "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC", "AC",
        "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD", "AD"]
   
    Deal()

    is_finished = PreFlopBets()
    if is_finished:
        AwardPot()
        NextHand()
        return

    PrintTableSituation()
    Flop()
    is_finished = BettingRound()  
    if is_finished:
        AwardPot()
        NextHand()
        return
    RiverOrTurn(turn=True)
    is_finished = BettingRound()  
    if is_finished:
        AwardPot()
        NextHand()
        return
    RiverOrTurn(turn=False)
    is_finished = BettingRound()  
    if is_finished:
        AwardPot()
        NextHand()
        return

    #Check who won, announce it, reward it
    AwardPot() 
    NextHand()
    return


def Game():
    table = []
    for i in range(0, num_players): table.append(Player(i, []))
    table[0].isBTN = True
    while(1):            
        Hand(table)
        left = 0
        for i in range(0, len(table)):
            if table[i].chips <= 0:
                table[i].inTheGame = False

            if table[i].inTheGame:
                left+=1
                index = i
        if left == 1:
            print(f"Player {index} won")
            return

        print("Next hand starting soon")
        time.sleep(3)
    

Game()
