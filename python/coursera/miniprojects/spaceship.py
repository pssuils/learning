#Mini-project #7
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
SPIN_VELOCITY = 0.01
CLOCK = True
ANTICLOCK = False
shooted = False

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
	for d in range(len(screen_size)):
		position[d] = (position[d] + velocity[d]) % screen_size[d]

	return position


def friction_down(velocity, friction):
	for d in range(len(velocity)):
		if abs(velocity[d]) > 0.00001 :
			velocity[d] *= (1 - friction)
		else:
			velocity[d] = 0

	return velocity


def speed_up(velocity, forward, k = 1):
	speed = list(velocity)
	for d in range(len(velocity)):
		speed[d] += (forward[d] * k)

	return speed

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

	def draw(self,canvas):
		image_center = self.image_center
		if self.thrust:
			image_center = (self.image_center[0] + self.image_size[0], self.image_center[1])

		canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)

	def update(self):
		self.angle += self.angle_vel

		self.vel = friction_down(self.vel, 0.01)

		if self.thrust:
			forward = angle_to_vector(self.angle)
			self.vel = speed_up(self.vel, forward, 0.2)		

		self.pos = move(self.pos, self.vel, [WIDTH, HEIGHT])

	def spin(self, clock = True):
		if clock:
			self.angle_vel += SPIN_VELOCITY
		else:
			self.angle_vel -= SPIN_VELOCITY 

	def stop_spin(self):
		self.angle_vel = 0

	def set_thrust(self, on = True):
		if on:
			self.thrust = True
			ship_thrust_sound.play()
		else:
			self.thrust = False
			ship_thrust_sound.rewind()

	def shoot(self):
		global a_missile, shooted
		shooted = True
		#The missile's initial position should be the tip of your ship's "cannon".
		forward = angle_to_vector(self.angle)
		position = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
		#Its velocity should be the sum of the ship's velocity and a multiple of the ship's forward vector.
		velocity = speed_up(self.vel, angle_to_vector(self.angle), 5)
		a_missile = Sprite(position, velocity, 0, 0, missile_image, missile_info, missile_sound)

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

	def draw(self, canvas):
		canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

	def update(self):
		self.angle += self.angle_vel
		self.pos = move(self.pos, self.vel, [WIDTH, HEIGHT])


def draw(canvas):
	global time

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
	a_rock.draw(canvas)
	if shooted:
		a_missile.update()
		a_missile.draw(canvas)

	# update ship and sprites
	my_ship.update()
	a_rock.update()

	canvas.draw_text('Lives : '+str(lives), (20, 30), 30, 'Red')
	canvas.draw_text('Score : '+str(score), (WIDTH - 150, 30), 30, 'Green')

# timer handler that spawns a rock	
def rock_spawner():
	global a_rock
	velocity = [random.randrange(-1, 1), random.randrange(-1, 1)]
	position = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
	angular_velocity = random.choice([0.1, 0.01, 0.05, -0.1, -0.01, -0.05])
	a_rock = Sprite(position, velocity, 0, angular_velocity, asteroid_image, asteroid_info)


def keydown(key): 
	if key==simplegui.KEY_MAP["right"]:
		my_ship.spin(CLOCK)
	if key==simplegui.KEY_MAP["left"]:
		my_ship.spin(ANTICLOCK)
	if key==simplegui.KEY_MAP["up"]:
		my_ship.set_thrust(True)

	if key==simplegui.KEY_MAP['space']:
		my_ship.shoot()


def keyup(key):
	if key==simplegui.KEY_MAP["right"] or key==simplegui.KEY_MAP["left"]:
		my_ship.stop_spin()
	if key==simplegui.KEY_MAP["up"]:
		my_ship.set_thrust(False)


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, asteroid_image, asteroid_info)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
