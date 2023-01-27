import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

class Card():  
    
    def __init__(self, suit,rank):
        
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck():
    
    def __init__(self):
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
    
    def __str__(self):
        card_dec = ''
        for card in self.all_cards:
            card_dec += '\n' + card.__str__()
        return f'The Deck has {card_dec}'
    
    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

class Hand():
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():
    
    def __init__(self, total=100):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input('How many chips do you want to bet?: '))
        except:
            print('Sorry, please provide an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry you do not have enough chips, you currently have {}'.format(chips.total))
            else:
                break

def hit(deck,hand):
    single_card = deck.deal_one()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = input('Hit or stand? h or s: ')
        
        if x == 'h':
            hit(deck,hand)
        
        elif x == 's':
            print('Player stands, dealers turn')
            playing = False
        else:
            print('Invalid')
        
        break

def show_some(player,dealer):
    print('\n Dealers hand: ')
    print('First card Hidden')
    print(dealer.cards[1])
    print(' ')
    
    print('\n Player hand: ')
    for card in player.cards:
        print(card)
    print(' ')
    
def show_all(player,dealer):
    print('\n Dealer hand: ')
    for card in dealer.cards:
        print(card)
    print(' ')
    print('Value of Dealers hand is: {}'.format(dealer.value))
    
    print('\n Player hand: ')
    for card in player.cards:
        print(card)
    print(' ')
    print('Value of Players hand is: {}'.format(player.value))

def player_busts(player,dealer,chips):
    print('Player busts')
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('Player wins')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('Player wins')
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print('Player loses')
    chips.lose_bet()
    
def push(player,dealer):
    print('Player and Dealer tie')

while True:
    print('Welcome to Black Jack')
    
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(deck.deal_one())
    player_hand.add_card(deck.deal_one())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())
    
    player_chips = Chips()
    
    take_bet(player_chips)
    
    show_some(player_hand, dealer_hand)
    
    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand, player_chips)
        break
        
    if player_hand.value <= 21:
        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)
        show_all(player_hand, dealer_hand)
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)     
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    print('\n player chips: {}'.format(player_chips.total))
    new_game = input('Want to play again, y or n: ')
    
    if new_game == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing, bye')
        break