#Mini-project #8 (Finale)
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

# globals for constants
ROCK_LIMIT = 12
SPIN_VELOCITY = 0.05
CLOCK = True
ANTICLOCK = False
started = False

class ImageInfo:
	def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
		self.center = center
		self.size = size
		self.radius = radius
		if lifespan:
			self.lifespan = lifespan
		else:
			self.lifespan = float('inf')
		self.animated = animated

	def get_center(self):
		return self.center

	def get_size(self):
		return self.size

	def get_radius(self):
		return self.radius

	def get_lifespan(self):
		return self.lifespan

	def get_animated(self):
		return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#				 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
	return [math.cos(ang), math.sin(ang)]


def dist(p,q):
	return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


def move(position, velocity, screen_size):
	"""
	Move an object inside the screen
	"""
	for d in range(len(screen_size)):
		position[d] = (position[d] + velocity[d]) % screen_size[d]

	return position


def friction_down(velocity, friction):
	"""
	Slow down the velocity
	"""
	for d in range(len(velocity)):
		if abs(velocity[d]) > 0.00001 :
			velocity[d] *= (1 - friction)
		else:
			velocity[d] = 0

	return velocity


def speed_up(velocity, forward, k = 1):
	"""
	Speed up the velocity
	"""
	speed = list(velocity)
	for d in range(len(velocity)):
		speed[d] += (forward[d] * k)

	return speed


def process_sprite_group(group, canvas):
	"""
	Update and draw the sprites if they are alive
	"""
	#to_remove = set([])
	for sprite in set(group):
		if(sprite.update()):
			sprite.draw(canvas)
		else:
			group.discard(sprite)

#rocks vs myship --- missiles vs rock
def group_collide(group, other, explosions):
	"""
	Get to know if an object collide with a group of objects
	"""
	collide = False
	for part in set(group):
		if part.collide(other):
			group.discard(part)
			explosions.add(Sprite(part.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
			collide = True

	return collide

#rocks vs missiles if collide one against other both dissapear
def group_group_collide(group1, group2, explosions):
	"""
	Count and eliminate the objects that are colliding with each other
	"""
	how_many = 0
	for part in set(group1):
		if group_collide(group2, part, explosions):
			group1.discard(part)
			how_many += 1

	return how_many

# Ship class
class Ship:
	def __init__(self, pos, vel, angle, image, info):
		self.pos = [pos[0],pos[1]]
		self.vel = [vel[0],vel[1]]
		self.thrust = False
		self.angle = angle
		self.angle_vel = 0
		self.image = image
		self.image_center = info.get_center()
		self.image_size = info.get_size()
		self.radius = info.get_radius()

	def get_position(self):
		return self.pos

	def get_radius(self):
		return self.radius

	def draw(self,canvas):
		image_center = list(self.image_center)
		if self.thrust:
			image_center[0] += self.image_size[0]

		canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)

	def update(self):
		#spin
		self.angle += self.angle_vel

		#slow down
		self.vel = friction_down(self.vel, 0.01)

		#speed up
		if self.thrust:
			forward = angle_to_vector(self.angle)
			self.vel = speed_up(self.vel, forward, 0.2)		

		#move it!
		self.pos = move(self.pos, self.vel, [WIDTH, HEIGHT])


	def spin(self, clock = True):
		if clock:
			self.angle_vel += SPIN_VELOCITY
		else:
			self.angle_vel -= SPIN_VELOCITY 

	def stop_spin(self):
		self.angle_vel = 0

	def set_thrust(self, on = True):
		self.thrust = on
		if on:
			ship_thrust_sound.play()
		else:
			ship_thrust_sound.rewind()

	def shoot(self, group):
		#The missile's initial position should be the tip of your ship's "cannon".
		forward = angle_to_vector(self.angle)
		position = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
		#Its velocity should be the sum of the ship's velocity and a multiple of the ship's forward vector.
		velocity = speed_up(self.vel, forward, 6)
		group.add(Sprite(position, velocity, 0, 0, missile_image, missile_info, missile_sound))


# Sprite class
class Sprite:
	def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
		self.pos = [pos[0],pos[1]]
		self.vel = [vel[0],vel[1]]
		self.angle = ang
		self.angle_vel = ang_vel
		self.image = image
		self.image_center = info.get_center()
		self.image_size = info.get_size()
		self.radius = info.get_radius()
		self.lifespan = info.get_lifespan()
		self.animated = info.get_animated()
		self.age = 0
		if sound:
			sound.rewind()
			sound.play()

	def get_position(self):
		return self.pos

	def get_radius(self):
		return self.radius

	def draw(self, canvas):
		if self.animated:
			center = [self.image_center[0] + ((self.age -1) * self.image_size[0]), self.image_center[1]]
			canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
		else:		
			canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

	def update(self):
		self.age += 1
		if self.age > self.lifespan:
			return False

		self.angle += self.angle_vel
		self.pos = move(self.pos, self.vel, [WIDTH, HEIGHT])
		return True

	def collide(self, other):
		if dist(self.pos, other.get_position()) > (self.radius + other.get_radius()):
			return False

		return True


def draw(canvas):
	global time, started, lives, score, missile_group, rock_group, explosion_group

	# animiate background
	time += 1
	wtime = (time / 4) % WIDTH
	center = debris_info.get_center()
	size = debris_info.get_size()
	canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
	canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
	canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

	# draw ship and sprites
	my_ship.draw(canvas)

	# update ship and sprites
	my_ship.update()
	process_sprite_group(missile_group, canvas)
	process_sprite_group(rock_group, canvas)
	process_sprite_group(explosion_group, canvas)

	#score and lives
	score += group_group_collide(rock_group, missile_group, explosion_group)
	if group_collide(rock_group, my_ship, explosion_group):
		lives -= 1

	if lives < 1 :
		started = False
		rock_group = set([])
		missile_group = set([])


	# draw UI
	canvas.draw_text("Lives", [50, 50], 22, "Red")
	canvas.draw_text("Score", [680, 50], 22, "Green")
	canvas.draw_text(str(lives), [50, 80], 22, "Red")
	canvas.draw_text(str(score), [680, 80], 22, "Green")

	# draw splash screen if not started
	if not started:
		canvas.draw_image(splash_image, splash_info.get_center(), 
				splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
				splash_info.get_size())


		#keyboard handlers		
def keydown(key): 
	if key==simplegui.KEY_MAP["right"]:
		my_ship.spin(CLOCK)
	elif key==simplegui.KEY_MAP["left"]:
		my_ship.spin(ANTICLOCK)

	if key==simplegui.KEY_MAP["up"]:
		my_ship.set_thrust(True)

	if key==simplegui.KEY_MAP['space']:
		my_ship.shoot(missile_group)


def keyup(key):
	if key==simplegui.KEY_MAP["right"] or key==simplegui.KEY_MAP["left"]:
		my_ship.stop_spin()

	if key==simplegui.KEY_MAP["up"]:
		my_ship.set_thrust(False)


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
	global started, score, lives, my_ship
	center = [WIDTH / 2, HEIGHT / 2]
	size = splash_info.get_size()
	inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
	inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
	if (not started) and inwidth and inheight:
		my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
		started = True
		score = 0
		lives = 3
		soundtrack.rewind()
		soundtrack.play()


# timer handler that spawns a rock	
def rock_spawner():
	if started and len(rock_group) < ROCK_LIMIT:
		velocity = [random.randrange(-1, 1), random.randrange(-1, 1)]
		angular_velocity = random.choice([0.1, 0.01, 0.05, -0.1, -0.01, -0.05])

		position = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
		while dist(position, my_ship.get_position()) < (my_ship.get_radius() + asteroid_info.get_radius()):
			position = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)];

		rock_group.add(Sprite(position, velocity, 0, angular_velocity, asteroid_image, asteroid_info))


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship 
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
