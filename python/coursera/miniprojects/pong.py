#Mini-project #4
import simplegui, random

# initialize globals constants
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ACCELERATION_PADDLE = 2
PADDLE_LEFT_X = HALF_PAD_WIDTH
PADDLE_RIGTH_X = WIDTH - HALF_PAD_WIDTH
SCORE_LEFT_POS = [WIDTH/4, 50]
SCORE_RIGHT_POS = [3*WIDTH/4, 50]

global ball_pos, ball_vel, paddle_left_y, paddle_right_y, paddle_left_vel, paddle_right_vel, score_left, score_rigth

def setup():
	"""
	Initializes the global positions, velocities and scores
	"""
	global ball_pos, ball_vel, paddle_left_y, paddle_right_y, paddle_left_vel, paddle_right_vel, score_left, score_rigth
	# initialize position and velocity of the ball in middle of table
	ball_pos = [WIDTH/2, HEIGHT/2]
	ball_vel = [0, 0]
	# initialize paddles in their side middle table, upper & bottom points of the line 
	paddle_left_y = [HEIGHT/2 - HALF_PAD_HEIGHT, HEIGHT/2 + HALF_PAD_HEIGHT]
	paddle_right_y = [HEIGHT/2 - HALF_PAD_HEIGHT, HEIGHT/2 + HALF_PAD_HEIGHT]
	# vertical (y) velocity of the paddles
	paddle_left_vel = paddle_right_vel = 0
	# initialize scores
	score_left = score_rigth =0


def update_position_paddle(vertical_position, vertical_velocity):
	"""
	Updates the next position of the paddle inside of the canvas
	"""
	if vertical_position[0] + vertical_velocity > -1 and vertical_position[1] + vertical_velocity < HEIGHT:
		vertical_position[0] += vertical_velocity
		vertical_position[1] += vertical_velocity

def hit_paddle(ball_pos, vertical_position):
	"""
	Calculate if the ball hit the paddle 
	"""
	return vertical_position[0] <= ball_pos[1] and ball_pos[1] <= vertical_position[1]

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
	"""
	Spawns a ball from the center to the upper direction
	"""
	global ball_pos, ball_vel 
	ball_pos = [WIDTH/2, HEIGHT/2]

	#random velocity per second
	ball_vel = [random.randrange(120, 240) // 60, - random.randrange(60, 180) // 60]

	if not direction:
		ball_vel[0] = -ball_vel[0]

def speed_up_ball():
	"""
	Speeding the ball 
	"""
	ball_vel[0] += ball_vel[0] * 0.10
	ball_vel[1] += ball_vel[1] * 0.10

# define event handlers

def new_game():
	"""
	Starts a new game with the ball randomly to the left or the right
	"""
	setup()
	random.seed()
	if random.randint(0, 1) == 0:
		spawn_ball(LEFT)
	else:
		spawn_ball(RIGHT)

def draw(canvas):
	"""
	Draws all the elements on the canvas
	"""
	global score_left, score_rigth

	# draw mid line and gutters
	canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
	canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
	canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

	# update ball
	ball_pos[0] += ball_vel[0]
	ball_pos[1] += ball_vel[1]

	#spawn(gutters) or collide & reflect on paddle
	if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
		if hit_paddle(ball_pos, paddle_left_y):
			ball_vel[0] = - ball_vel[0]
			peed_up_ball() 
		else:
			score_rigth += 1
			spawn_ball(RIGHT)
	elif ball_pos[0] >= WIDTH - 1 - BALL_RADIUS - PAD_WIDTH:
		if hit_paddle(ball_pos, paddle_right_y):
			ball_vel[0] = - ball_vel[0] 
			speed_up_ball() 
		else:
			score_left += 1
			spawn_ball(LEFT)	

	#collide & reflect top & bottom (not problem if it's been spawned)
	if ball_pos[1] <= BALL_RADIUS:
		ball_vel[1] = - ball_vel[1]
	elif ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS:
		ball_vel[1] = - ball_vel[1]

	# draw ball
	canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

	# update:paddle's vertical position, keep paddle on the screen
	update_position_paddle(paddle_left_y, paddle_left_vel)
	update_position_paddle(paddle_right_y, paddle_right_vel)


	# draw paddles
	points = [(PADDLE_LEFT_X, paddle_left_y[0]),(PADDLE_LEFT_X, paddle_left_y[1])]
	canvas.draw_line(points[0], points[1], PAD_WIDTH, 'WIDTH')
	points = [(PADDLE_RIGTH_X, paddle_right_y[0]),(PADDLE_RIGTH_X, paddle_right_y[1])]
	canvas.draw_line(points[0], points[1], PAD_WIDTH, 'WIDTH')

	# draw scores
	canvas.draw_text(str(score_left), SCORE_LEFT_POS, 30, 'Green', 'serif')
	canvas.draw_text(str(score_rigth), SCORE_RIGHT_POS, 30, 'Green', 'serif')

def keydown(key):
	"""
	Increases the velocity of each paddle if pressed key correct
	"""
	global paddle_left_vel, paddle_right_vel

	if key==simplegui.KEY_MAP["up"]:
		paddle_right_vel -= ACCELERATION_PADDLE
	elif key==simplegui.KEY_MAP["down"]:
		paddle_right_vel += ACCELERATION_PADDLE

	if key==simplegui.KEY_MAP["s"]:
		paddle_left_vel += ACCELERATION_PADDLE
	elif key==simplegui.KEY_MAP["w"]:
		paddle_left_vel -= ACCELERATION_PADDLE

def keyup(key):
	global paddle_left_vel, paddle_right_vel
	"""
	Stops each paddle if the correspondent key is released
	"""

	if key==simplegui.KEY_MAP["up"] or key==simplegui.KEY_MAP["down"]:
		paddle_right_vel = 0

	if key==simplegui.KEY_MAP["s"] or key==simplegui.KEY_MAP["w"]:
		paddle_left_vel = 0

def reset():
	"""
	Resets the game
	"""
	new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', reset, 150)


# start frame
new_game()
frame.start()
