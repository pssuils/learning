#Mini-project #5
import simplegui
import random

N_CARDS = 8
CARD = 50
HEIGHT = 100
FONT = HEIGHT/2
WIDTH = N_CARDS * CARD * 2
DECK = range(N_CARDS)
NO_CARDS = 0
CARD_ONE = 1
CARD_TWO = 2

cards = []
exposed = []
open_cards = []
state = NO_CARDS
turn = 0

#helpers
def get_cards_points(index):
	"""
	4 points of the card according to the index of the card
	"""
	shift = index * CARD
	return [(shift, 0),(shift, HEIGHT),(shift + CARD, HEIGHT),(shift + CARD, 0)]


def get_card_position(index):
	"""
	the position of the text of the card
	"""
	return (index * CARD + 10, 4*FONT/3)	


def index_of_card_clicked(x):
	"""
	from a x position of the canvas get the index of the card
	"""
	return x // CARD


def new_game():
	"""
	Starts a new game reseting every global
	"""
	global cards, exposed, turn

	state = NO_CARDS
	turn = 0

	random.seed()
	cards = DECK + DECK
	random.shuffle(cards)
	exposed = [False for card in cards]


# define event handlers
def mouseclick(pos):
	"""
	expose or not the card click on and count the turns
	"""
	global state, turn

	card_clicked = index_of_card_clicked(pos[0])

	if not exposed[card_clicked]:
		if state == CARD_TWO:
			c1 = open_cards.pop()
			c2 = open_cards.pop()

			if cards[c1] != cards[c2]:
				exposed[c1], exposed[c2] = False, False

		open_cards.append(card_clicked)
		exposed[card_clicked] = True

		if state == NO_CARDS:
			state = CARD_ONE
		elif state == CARD_ONE:
			turn += 1
			state = CARD_TWO
		else:
			state = CARD_ONE


def draw(canvas): 
	"""
	Draw the turn counter and the cards exposed or not
	"""
	label.set_text("Turns = "+str(turn))

	for index, card in enumerate(cards):
		if exposed[index]:
			canvas.draw_text(str(card), get_card_position(index), FONT, "white", "serif")
		else:
			canvas.draw_polygon(get_cards_points(index), 1, "Red", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
