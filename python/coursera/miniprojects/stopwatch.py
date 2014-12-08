#Mini-project #3
import simplegui

# define global variables
time = 0
succesful_stops = 0
total_stops = 0
stopped = True

#helpers
def format(t):
	"""
	Converts time in tenths of seconds to A:BC.D
	"""
	A = t // 600

	remainder = t % 600
	BC = remainder // 10

	remainder %= 10
	D = remainder%10

	time_string = str(A)+(':')
	if BC < 10:
		time_string += '0'

	time_string += str(BC)+'.'+ str(D)

	return time_string

def getStrScore():
	"""
	Gets the score as a string
	"""
	return str(succesful_stops) + ' / ' + str(total_stops)

def updateScore():
	"""
	Updates the score being succes if it's in a whole second
	"""
	global succesful_stops, total_stops

	total_stops += 1
	if time % 10 == 0:
		succesful_stops += 1

#handlers
def start():
	"""
	Starts the timer
	"""
	global stopped
	if stopped:
		timer.start()
		stopped = False

def stop():
	"""
	Stops the timer and updates the score
	"""
	global stopped
	if not stopped:
		timer.stop()
		stopped = True
		updateScore()

def reset():
	"""
	Resets the game
	"""
	global time, succesful_stops, total_stops, stopped
	time = 0
	succesful_stops = 0
	total_stops = 0

	if not stopped:
		timer.stop()
		stopped = True

def tick():
	"""
	Counts the time
	"""
	global time
	time += 1

def prints(canvas):
	"""
	Prints the time and the score
	"""
	canvas.draw_text(format(time), (60, 115), 40, 'White')
	canvas.draw_text(getStrScore(), (140, 30), 20, 'Green')

# create frame
frame = simplegui.create_frame('StopWatch', 200, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
start = frame.add_button('Start', start, 150)
stop = frame.add_button('Stop', stop, 150)
stop = frame.add_button('Reset', reset, 150)
frame.set_draw_handler(prints)

# start frame
frame.start()
