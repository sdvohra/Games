# Shriya Vohra, 12-01-15

# This is a Python 2 script and is fully executable in a Python Shell.
# Enjoy!

# This Blackjack game allows the following options:
# - Money
# - Natural BJ (Pay)
# - Double Down
# - Dealer BJ
# - Dealer Ace Showing (Insurance/Even Money)

#import games, random

class Card(object):
    """ A playing card. """
    RANKS = ["A", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "J", "Q", "K"]
    SUITS = ["S", "H", "D", "C"]

    def __init__(self, rank, suit, face_up = True):
        self.rank = rank 
        self.suit = suit
        self.is_face_up = face_up

    def __str__(self):
        if self.is_face_up:
            stringRep = self.rank + self.suit
        else:
            stringRep = "XX"
        return stringRep

    def flip(self):
        self.is_face_up = not self.is_face_up

class Hand(object):
    """ A hand of playing cards. """
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        if self.cards:  # if contains values
           stringRep = ""
           for card in self.cards:
               stringRep += str(card) + "\t"
        else:
            stringRep = "Empty!"
        return stringRep
    
    def clear(self):
        self.cards = []
        
    def add(self, card):
        self.cards.append(card) # append is built-in
        
    def give(self, card, other_hand):
        self.cards.remove(card) # remove is built-in
        other_hand.add(card)
        
class Deck(Hand):   # EXTENDS HAND
    """ A deck of playing cards. """
    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS: 
                self.add(BJ_Card(rank, suit))  # adds to cards[]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            if self.cards:  # if deck has cards
                top_card = self.cards[0]
                self.give(top_card, hands)
            else:
                print "Can't continue deal. Out of cards!"

class BJ_Card(Card):    # EXTENDS CARD
    """ A Blackjack Card. """
    def get_value(self):
        if self.is_face_up:
            value = BJ_Card.RANKS.index(self.rank) + 1
            if value > 10:
                value = 10
        else:
            value = None
        return value

    value = property(get_value)

class BJ_Hand(Hand):    # EXTENDS HAND
    """ A Blackjack Hand. """
    def get_total(self):
        total = 0
        contains_ace = False
        for card in self.cards:
            if not card.value:
                return None
            total = total + card.value
            if (card.value == 1):
                contains_ace = True
        if contains_ace and total <= 11:
            total += 10
        return total

    total = property(get_total)
    
    def is_busted(self):
        return self.total > 21

class BJ_Player(object):
    """ A Blackjack Player. """
    def __init__(self, name):
        self.player_name = name
        self.hand = BJ_Hand()
        self.stillPlaying = True
        self.isBusted = False
        self.noMoney = False
        self.naturalBJ = False
        self.insurance = False
        self.evenMoney = False
        self.balance = 200
        self.bet = 10
    
    def __str__(self):
        return "Name: "+str(self.player_name)+"\nHand: "+str(self.hand)+"\nBalance: "+str(self.balance)

class BJ_Dealer(object):
    """ A Blackjack Dealer. """
    def __init__(self):
        self.hand = BJ_Hand()
        self.dNaturalBJ = False
    
    def __str__(self):
        return "Name: DEALER"+"\nHand: "+str(self.hand)

class BJ_Game(object):
    """ A Blackjack Game. """
    def __init__(self):      
        self.players = []
        self.dealer = BJ_Dealer()
        self.deck = Deck()

    def get_still_playing(self):
        temp = []
        for player in self.players:
            if (player.stillPlaying):
                temp.append(player)
        return temp

    def welcome(self):
        print "Welcome to Blackjack!"

        num = games.ask_number(question = "How many players? (2 - 5): ",
                                       low = 2, high = 6)
        for i in range(num):
            name = raw_input("Player " + str(i+1) + "'s Name: ")
            player = BJ_Player(name)
            self.players.append(player)

    def setup(self):
        # Populate & Shuffle deck
        self.deck.populate()
        self.deck.shuffle()
        
        # Deal initial 2 cards to everyone
        for player in self.players:
            self.deck.deal(player.hand, 2)

        # Deal cards (1 face up, 1 face down) to dealer
        self.deck.deal(self.dealer.hand, 2)
        self.dealer.hand.cards[1].flip()

    def display_players(self):
        for player in self.players:
            print "- - - - - - - - - - - - - -"
            print player
            print "- - - - - - - - - - - - - -"

    def display_dealer(self):
        print self.dealer
    
    def play(self):
        print
        print "GAME BEGINS:"
        print

        # Ask for bets
        for player in self.players:
            bet = -1
            while (bet <= 0 or bet > player.balance):
                bet = int(raw_input(str(player.player_name) + ": How much would you like to bet? "))
            player.bet = bet
            player.balance = player.balance - bet

        # Show cards dealt
        print
        print "CARDS DEALT:"
        print
        self.display_dealer()
        self.display_players()
        
        # Check for natural blackjack
        for player in self.players:
            if (player.hand.get_total() == 21):
                player.stillPlaying = False
                player.naturalBJ = True

        # Check dealer's face up card for 10, J, Q, or K
        if (self.dealer.hand.cards[0].rank == "10" or self.dealer.hand.cards[0].rank == "J" or self.dealer.hand.cards[0].rank == "Q" or self.dealer.hand.cards[0].rank == "K"):
            self.dealer.hand.cards[1].flip()
            if (self.dealer.hand.get_total() == 21):
                print "Dealer has Natural Blackjack!"
                self.dealer.dNaturalBJ = True
                for player in self.players:
                    player.stillPlaying = False
            self.dealer.hand.cards[1].flip()

        # Check dealer's face up card for A
        if (self.dealer.hand.cards[0].rank == "A"):
            # Ask if players want insurance / even money
            for player in self.players:
                if (not player.naturalBJ):
                    needToPrompt = True
                    while (needToPrompt):
                        answer = raw_input(str(player.player_name) + ": Insurance? (Y/N) ")
                        if (answer == "Y"):
                            if (player.balance - (player.bet/2) < 0):
                                print "Not enough money! Choose another option."
                            else:
                                player.balance = player.balance - (player.bet/2)
                                player.insurance = True
                                needToPrompt = False
                        else:
                            needToPrompt = False
                else:
                    needToPrompt = True
                    while (needToPrompt):
                        answer = raw_input(str(player.player_name) + ": Even Money? (Y/N) ")
                        if (answer == "Y"):
                            if (player.balance - (player.bet/2) < 0):
                                print "Not enough money! Choose another option."
                            else:
                                player.evenMoney = True
                                needToPrompt = False
                        else:
                            needToPrompt = False
            self.dealer.hand.cards[1].flip()
            if (self.dealer.hand.get_total() == 21):
                print "Dealer has a Natural Blackjack!"
                self.dealer.dNaturalBJ = True
                for player in self.players:
                    if (player.insurance):
                        player.balance = player.balance + player.bet
                        player.stillPlaying = False
                    elif (player.evenMoney):
                        player.balance = player.balance + player.bet*2
                        player.stillPlaying = False
                    else:
                        player.stillPlaying = False
                self.dealer.hand.cards[1].flip()
            else:
                self.dealer.hand.cards[1].flip()
                
        for player in self.players:
            if (player.stillPlaying):
                print
                print "---------------------------"
                print player
                print "---------------------------"
                stand = False
                isBust = False

                iteration = 1
                while ((not isBust) and (not stand)):
                    if (iteration == 1):
                        answer = int(raw_input("Would you like to (1) Hit, (2) Stand, or (3) Double Down? "))
                        if (answer == 1):
                            top_card = self.deck.cards[0]
                            self.deck.give(top_card,player.hand)
                            print str(player)
                            isBust = player.hand.is_busted()
                        elif (answer == 2):
                            print "Stand. Your total is: " + str(player.hand.get_total())
                            stand = True
                        elif (answer == 3):
                            if (player.balance - bet < 0):
                                print "Not enough money to Double Down! Please select another option."
                                iteration = 0
                            else:
                                player.balance = player.balance - bet
                                player.bet = player.bet*2
                                top_card = self.deck.cards[0]
                                self.deck.give(top_card,player.hand)
                                print str(player)
                                isBust = player.hand.is_busted()
                                stand = True
                    else:
                        answer = int(raw_input("Would you like to (1) Hit or (2) Stand? "))
                        if (answer == 1):
                            top_card = self.deck.cards[0]
                            self.deck.give(top_card,player.hand)
                            print str(player)
                            isBust = player.hand.is_busted()
                        elif (answer == 2):
                            print "Stand. Your total is: " + str(player.hand.get_total())
                            stand = True
                    iteration = iteration + 1
                if (isBust):
                    print "You busted!"
                    player.isBusted = True
                    player.stillPlaying = False
                print "\nSwitching turns."
            elif (player.naturalBJ):
                print
                print "---------------------------"
                print "NATURAL BLACKJACK!"
                print player
                print "---------------------------"

        print "---------------------------"
        print "Time to reveal the dealers hand..."
        self.dealer.hand.cards[1].flip()
        self.display_dealer()

        print "Dealer plays."
        while (self.dealer.hand.get_total() < 17):
            top_card = self.deck.cards[0]
            self.deck.give(top_card,self.dealer.hand)
            self.display_dealer()
        if (self.dealer.hand.get_total() > 21):
            print "Dealer busts!\n"
        
        print "---------------------------"
        print "RESULTS:\n"

        if (self.dealer.hand.get_total() > 21): # Dealer busts
            for player in self.players:
                if (player.stillPlaying):
                    print "WINNER!"
                    player.balance = player.balance + player.bet*2
                    print player
                    print
                else:
                    if (player.isBusted):
                        print "LOSER! You busted."
                        print player
                        print
                    elif (player.noMoney):
                        print "LOSER! You ran out of $."
                        print player
                        print
                    elif (player.naturalBJ):
                        print "WINNER - NATURAL BLACKJACK!"
                        player.balance = player.balance + player.bet*2.5
                        print player
                        print
        else:
            for player in self.players:
                if (not player.evenMoney):
                    if (player.isBusted):
                        print "LOSER! You busted."
                        print player
                        print
                    elif (player.noMoney):
                        print "LOSER! You ran out of $."
                        print player
                        print
                    elif (player.naturalBJ):
                        if (not self.dealer.dNaturalBJ):
                            print "WINNER - NATURAL BLACKJACK!"
                            player.balance = player.balance + player.bet*2.5
                            print player
                            print
                        else:
                            print "TIE!"
                            player.balance = player.balance + player.bet
                            print player
                            print
                    else:
                        if (player.hand.get_total() > self.dealer.hand.get_total()):
                            print "WINNER!"
                            player.balance = player.balance + player.bet*2
                            print player
                            print
                        elif (player.hand.get_total() == self.dealer.hand.get_total()):
                            print "TIE!"
                            player.balance = player.balance + player.bet
                            print player
                            print
                        else:
                            print "LOSER!"
                            print player
                            print
                else:
                    print "WINNER - EVEN MONEY!"
                    print player
                    print

# main
game = BJ_Game()
game.welcome()
game.setup()
game.play()
