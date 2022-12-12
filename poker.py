import random
import time 

#ToDo's:
#1-->betting system (Pre-Flop: Done) (Post-Flop, Post-Turn, Post-River: ToDo)
#2-->blind increase system (time)
#3-->card deal (Private Cards: Done) (Flop, Turn, River: ToDo)
#4-->check who won

#Setting game variables:
num_players = 9


class Player:
    inTheHand = True
    inTheGame = True
    isBTN = False
    lastAction = False
    starting_chips = 5000
    cur_bet = 0
    blinds = 30 #(BB)
    min_bet = 0 #Keep track of the min bet
    pot = 0

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
        bet = int(input(f"{Player.min_bet} is the min bet. You have {self.chips}Raise to: "))
        if self.chips>=bet:
            if bet >= Player.min_bet + Player.blinds:
                Player.pot += bet - self.cur_bet
                self.chips -= bet
                self.cur_bet = bet
                Player.min_bet = bet
            else:
                print("Distancia de valor muito pequeno. Call")
                self.Call()
        else:
            print("All In")
            self.AllIn()

    def AllIn(self):
        self.cur_bet+=self.chips
        Player.pot += self.chips
        self.chips = 0
        if Player.min_bet < self.cur_bet:
            Player.min_bet = self.cur_bet
            
            
        print(f"Player {self.table_seat} is all in for {self.cur_bet}. Min bet now is {Player.min_bet}, player has {self.chips} chips left")
        return 1

    def Fold(self):
        self.inTheHand = False

def TableSituation(table):
    for player in table:
        print(f"Player {player.table_seat}: Chips = {player.chips}")
    print(f"Total pot: {Player.pot}")

def Hand(table):

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

    def BettingMenu(player):  
        print("")  
        min_before = Player.min_bet
        print(f"Player{player.table_seat}. You have: {player.chips}")
        print(f"Min bet is {Player.min_bet}, you already have {player.cur_bet} on the table")
        choice = ""
        if player.cur_bet == Player.min_bet:
            while choice!="A" and choice!="C" and choice!="R":
                print("[A]: All in")
                print("[C]: Check")
                print("[R]: Raise")
                choice = input("Your decision:")
                if choice == "A": player.AllIn()
                if choice == "C": player.Check()
                if choice == "R": player.Raise()
                       
        elif player.cur_bet + player.chips <= Player.min_bet:
            while choice!="A" and choice!="F":
                print("[A]: All in")
                print("[F]: Fold")
                choice = input("Your decision:")
                if choice == "A": player.AllIn()
                if choice == "F": player.Fold()

        else:
            while choice!="A" and choice!="C" and choice!="R" and choice!="F":
                print("[A]: All in")
                print("[C]: Call")
                print("[R]: Raise")
                print("[F]: Fold")
                choice = input("Your decision:")
                if choice == "A": player.AllIn()
                if choice == "C": player.Call()
                if choice == "R": player.Raise()
                if choice == "F": player.Fold()
        if Player.min_bet > min_before:
            #Check the last action
            last_to_play = player.table_seat-1
            while(table[last_to_play].inTheHand==False):
                last_to_play -= 1
            print(f"Last to play should be {last_to_play}")
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
            if table[cur_player].inTheHand and table[cur_player].inTheGame: BettingMenu(table[cur_player])


            if table[cur_player].lastAction: break #If the lastAction does raise, lastAction--> table[cur_player-1]
            cur_player+=1
            
    deck = ["2A", "3A", "4A", "5A", "6A", "7A", "8A", "9A", "10A", "JA", "QA", "KA", "AA",
        "2B", "3B", "4B", "5B", "6B", "7B", "8B", "9B", "10B", "JB", "QB", "KB", "AB",
        "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
        "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD"]
    Deal() #Set the self.inTheHand to true for every one in the Game

    #for player in table:
    #    print(player.cards)

    PreFlopBets()
    TableSituation(table)


    RotateBTN()
    ResetLastAction()
    TakeCards()
    return

def Game():
    table = []
    for i in range(0, num_players): table.append(Player(i, []))
    table[0].isBTN = True
    while(1):
        Hand(table)
        input("")
    

Game()
