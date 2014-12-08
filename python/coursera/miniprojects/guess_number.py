#Mini-project #2
import simplegui, random, math

#Global Initializations
global secret_number, min_number, max_number, max_guesses
min_number = 0
max_number = 100

def new_game():
	"""
	Starts a new game with a new secret number and the maximum of guesses according to the range
	"""
	global secret_number, max_guesses

	secret_number = random.randrange(0, max_number)
	max_guesses = int(math.ceil(math.log(max_number - min_number + 1, 2)))

	print "\nNew game. Range is [%d, %d)"%(min_number, max_number)

	print "Number of remaining guesses is %d"%max_guesses

	return True

def range100():
	"""
	Starts a new game with a new secret within [0,100)
	"""
	global max_number
	max_number = 100

	return new_game()

def range1000():
	"""
	Starts a new game with a new secret within [0, 1000)
	"""
	global max_number
	max_number = 1000

	return new_game()

def input_guess(guess):
	"""
	Checks the user guess and gives feedback, starting a new game if the user guesses the correct number o run out of guesses tries
	"""
	global max_guesses

	max_guesses -= 1
	number_guess = int(guess)
	restarted = False

	print '\nGuess was %d'%number_guess

	if number_guess == secret_number:
		print "Correct!"
		restarted = new_game()
	elif number_guess < secret_number:
		print "Higher!"
	else:
		print "Lower!"

	if not restarted:
		if max_guesses < 1:
			print "You ran out of guesses.  The number was %d"%secret_number
			restarted = new_game()
		else:
			print "Number of remaining guesses is %d"%max_guesses

	return restarted

# create frame
frame = simplegui.create_frame('Guess A Number', 100, 200)

# register event handlers for control elements and start frame
bt1 = frame.add_button('Range: 0 - 100', range100, 150)
bt2 = frame.add_button('Range: 0 - 1000', range1000, 150)
inp = frame.add_input('Guess a Number', input_guess, 150)

# call new_game 
new_game()

# starting the game frame
frame.start()
