# Mini-project #6 - Blackjack
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")	

POS_DEALER = (50, 200)
POS_PLAYER = (50, 400)
CENTER_HOLE = (POS_DEALER[0] + CARD_CENTER[0], POS_DEALER[1] + CARD_CENTER[1])

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
	"""
	Card = RANK + SUIT
	"""
	def __init__(self, suit, rank):
		if (suit in SUITS) and (rank in RANKS):
			self.suit = suit
			self.rank = rank
		else:
			self.suit = None
			self.rank = None
			print "Invalid card: ", suit, rank

	def __str__(self):
		return self.suit + self.rank

	def get_suit(self):
		return self.suit

	def get_rank(self):
		return self.rank

	def draw(self, canvas, pos):
		card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
				CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
		canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
		
# define hand class
class Hand:
	"""
	Hand = array of cards
	"""
	def __init__(self):
		self.cards = []

	def __str__(self):
		ans = "Hand contains"
		for card in self.cards:
			ans += " "+ str(card)
		return ans

	def add_card(self, card):
		self.cards.append(card)

	def get_value(self):
		value = 0

		for card in self.cards:
			value += VALUES[card.get_rank()]

		for card in self.cards:
			if card.get_rank() == 'A' and value + 10 <= 21:
				value +=10
	
		return value
	
	
	def draw(self, canvas, pos):
		for card in self.cards:
			card.draw(canvas, pos)
			pos[0] += CARD_SIZE[0]
	
		
# define deck class 
class Deck:
	"""
	Deck class
	"""
	def __init__(self):
		self.cards = []
		for suit in SUITS:
			for rank in RANKS:
				self.cards.append(Card(suit, rank))
				

	def shuffle(self):
		random.shuffle(self.cards)

		
	def deal_card(self):
		return self.cards.pop(0)

	
	def __str__(self):
		ans = "Deck contains"
		for card in self.cards:
			ans += " "+ str(card)
		return ans



#define event handlers for buttons
def deal():
	"""
	Start the game
	"""
	global outcome, in_play, deck, player, dealer, message, score


	player = Hand()
	dealer = Hand()
	deck = Deck()
	deck.shuffle()
	
	for i in range(2):
		dealer.add_card(deck.deal_card())
		player.add_card(deck.deal_card())
	
	if in_play:
		score -= 1
		outcome = "You Lost!! Hit or Stand?"
	else:
		outcome = "Hit or Stand?"
	
	in_play = True


def hit():
	"""
	Another card
	"""
	global deck, player, dealer, in_play, outcome, score

	if in_play:
		player.add_card(deck.deal_card())
	
	if player.get_value() > 21:
		in_play = False
		outcome = "You Have Busted!! New Deal?"
		score -= 1
 

def stand():
	"""
	Stop time for the croupier hand
	"""
	global deck, player, dealer, in_play, outcome, score
	
	player_v = player.get_value()
	
	
	if player_v > 21:
		outcome = "You Have Busted!! New Deal?"
	elif in_play:
		while(dealer.get_value() < 17):
			dealer.add_card(deck.deal_card())

		dealer_v = dealer.get_value()
		
		if dealer_v > 21 or player_v > dealer_v:
			outcome = "You Win!! New Deal?"
			score += 1
		else:
			outcome = "You Lost!! New Deal?"
			score -= 1
		
		in_play = False
			

	
# draw handler	
def draw(canvas):
	global player, dealer
	
	dealer.draw(canvas, list(POS_DEALER))
	player.draw(canvas, list(POS_PLAYER))

	if in_play:
		canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, CENTER_HOLE, CARD_SIZE)
	else: 
		res = "Player : "+str(player.get_value())
		canvas.draw_text(res, (5,20), 20, "Grey")
		res = "Dealer : "+str(dealer.get_value())
		canvas.draw_text(res, (5,40), 20, "Grey")

	canvas.draw_text('Blackjack', (400, 50), 40, 'Black', 'serif')
	canvas.draw_text("Score : "+str(score), (400, 100), 34, 'Black', 'serif')
	canvas.draw_text(outcome, (300, 350), 24, 'Black', 'serif')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
