import random
import simplegui

""" PyGame Blackjack
    An simple implementation of Blackjack (aka 21).

    N.b.: you may want to change the source of the image files. The two images
    represent the card faces and the card backs. As long as the dimentions are the same,
    you can replace the images to something else.
"""

__author__ = ('Dee Reddy', 'deesus@yandex.com')

#############################################


# load card sprite - 936x384
card_images = simplegui.load_image("https://raw.githubusercontent.com/Deesus/PyGame-Games/master/blackjack/card_faces.png")
card_backs = simplegui.load_image("https://raw.githubusercontent.com/Deesus/PyGame-Games/master/blackjack/card_backs.png")

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
global_score = 0
inPlay = False
global_text = "Hit or Stand?"

VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
SUITS = ('C', 'S', 'H', 'D')
playerHand = houseHand = None

########################################


class Card():
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + self.suit

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def draw(self, canvas, position):
        card_location = (CARD_CENTER[0] + CARD_SIZE[0]*RANKS.index(self.rank),
                         CARD_CENTER[1] + CARD_SIZE[1]*SUITS.index(self.suit))
        canvas.draw_image(card_images, 
                          card_location, CARD_SIZE, 
                          (position[0]+CARD_CENTER[0], position[1]+CARD_CENTER[1]),
                          CARD_SIZE)


class Deck():
    def __init__(self):
        global RANKS, SUITS

        self.atDeck = [[x,y] for x in RANKS for y in SUITS]

    def deal(self):
        random.shuffle(self.atDeck)
        self.index = 0

    def nextCard(self):
        self.index += 1
        x,y = self.atDeck[self.index-1][0], self.atDeck[self.index-1][1]
        return Card(x,y)


class Hand():
    def __init__(self, *cards):
        self.arrayCards = list(cards)
        self.value = sum([VALUES[cCard.getRank()] for cCard in self.arrayCards])

        if 'A' in [cCard.getRank() for cCard in self.arrayCards]: self.hasAce = True
        else: self.hasAce = False

    def __str__(self):
        return str([str(x) for x in self.arrayCards]) + '\n' + 'value: ' + str(self.getValue())

    def addCard(self, cCard):
        self.arrayCards.append(cCard)
        if cCard.getRank() == 'A': self.hasAce == True

        self.value += VALUES[cCard.getRank()]

    def getValue(self):
        if self.hasAce and self.value <= 11:
            return self.value + 10
        else:
            return self.value

#######################
# mouse click handler #
#######################

def deal():
    global deck, playerHand, houseHand, inPlay, global_text, global_score
    
    # pressing the "Deal" in middle of the round results in player losing round:
    if inPlay: global_score -= 1
    
    global_text = "Hit or Stand?"
    inPlay = True
    deck.deal()
    playerHand  = Hand(deck.nextCard(), deck.nextCard())
    houseHand   = Hand(deck.nextCard(), deck.nextCard())

def hit():
    global global_score, inPlay, global_text
    
    if playerHand.getValue() > 21:
        global_text = "You already busted."
        return
    elif not inPlay:
        global_text = "Deal card first."
        return

    if playerHand.getValue() <= 21:
        playerHand.addCard(deck.nextCard())
    if playerHand.getValue() > 21:
        inPlay = False
        
        global_text = "You busted! Deal Again?"
        global_score -= 1

def stand():
    global global_score, inPlay, global_text

    if not inPlay:
        global_text = "Your turn is over."
        return
    elif playerHand.getValue() > 21: 
        global_text = "You already busted."
        return
    inPlay = False

    while houseHand.getValue() < 17:
        houseHand.addCard(deck.nextCard())
    if houseHand.getValue() > 21: global_text = "House Busts!"

    if (houseHand.getValue() <= 21) and (houseHand.getValue() >= playerHand.getValue()):
        global_text = "House wins. Deal Again?"
        global_score -= 1
    else:
        global_text = "You win! Deal Again?"
        global_score += 1

################
# draw Handler #
################


def draw_handle(canvas):
    global inPlay
    # draw Player hand:
    i = 0
    for c in playerHand.arrayCards:
        c.draw(canvas, [10 + i*80, 400])
        i+= 1
     
    # draw Dealer's hand:
    i = 0
    for c in houseHand.arrayCards:
        if inPlay and i == 0:
            canvas.draw_image(card_backs, CARD_CENTER, CARD_SIZE, (10+CARD_CENTER[0], 100+CARD_CENTER[1]), CARD_SIZE)
        else:
            c.draw(canvas, [10 + i*80, 100])
        i+= 1
        
    # draw text:
    canvas.draw_text('Black Jack', (200, 50), 40, 'Black')
    canvas.draw_text('Dealer', (10, 230), 20, 'White')
    canvas.draw_text("Player", (10, 530), 20, 'White')
    canvas.draw_text("%s" % global_text, (230, 550), 20, '#A3E0FF')
    canvas.draw_text("Score: %d" % global_score, (10, 550), 20, "Black")
    
################
# create frame #
################ 

# create a frame and assign callbacks to event handlers:
frame = simplegui.create_frame("Home", 600, 600)
frame.set_canvas_background('#2E8B57')

frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)

frame.set_draw_handler(draw_handle)
frame.start()

################
#  start game  #
################ 

deck = Deck()
deal()
