import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
WINDOW = None
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

#### Put class definitions here ####


class Wall(GameElement):
	IMAGE = "Wall"
	SOLID = True

class Rock(GameElement):
	IMAGE = "Rock"
	SOLID = True

	def next_pos(self, direction):
		if direction == "up":
			return (self.x, self.y-1)
		elif direction == "down":
			return (self.x, self.y+1)
		elif direction == "left":
			return (self.x-1, self.y)
		elif direction == "right":
			return (self.x+1, self.y)
		return None
	def interact(self, direction):
		print "in interact method!"
		print direction


		next_location = self.next_pos(direction)
		next_x = next_location[0]
		next_y = next_location[1]

		
		existing_el = GAME_BOARD.get_el(next_x,next_y)
		print "existing_el is: " ,  existing_el

		if existing_el is None or not existing_el.SOLID and existing_el.IMAGE != "DoorOpen" and existing_el.IMAGE != "Rock":
			print "is this the error?"
			GAME_BOARD.del_el(self.x, self.y)
			GAME_BOARD.set_el(next_x, next_y, self)


		# next_x = self.x
		# next_y = self.y
		# if direction == "up":
		# 	return (self.x, self.y-1)
		# elif direction == "down":
		# 	return (self.x, self.y+1)
		# elif direction == "left":
		# 	return (self.x-1, self.y)
		# elif direction == "right":
		# 	next_x = self.x+1
		# 	next_y = self.y


		GAME_BOARD.del_el(self.x, self.y)
		GAME_BOARD.set_el(next_x, next_y, self)

		#return None

class Character(GameElement):
	IMAGE = "Horns"

	# determining next character position based on keyboard inputs below
	def next_pos(self, direction):
		if direction == "up":
			return (self.x, self.y-1)
		elif direction == "down":
			return (self.x, self.y+1)
		elif direction == "left":
			return (self.x-1, self.y)
		elif direction == "right":
			return (self.x+1, self.y)
		return None

	# initializing an inventory for each character
	def __init__(self):
		GameElement.__init__(self)
		self.inventory = []
		IMAGE = "Horns"

class Magic(GameElement):
	IMAGE = "Princess"
	SOLID = True

class Gem(GameElement):
	IMAGE = "BlueGem"
	SOLID = False

	# adding each gem to the player's inventory
	def interact(self, player):
		player.inventory.append(self)
		GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

# we made the player reset their original position after they found the door!!!!!
class Door_Reset_Player(GameElement):
	IMAGE = "DoorOpen"
	SOLID = False

	# specifically: we delete current player, reset them to original position,
	# then delete the door element

	def on_key_press(self, symbol, modifiers):
		if KEYBOARD[key.ENTER]:
		# if symbol == key.ENTER:
			GAME_BOARD.draw_msg("You went through a door!")
			print chr(7)
			GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
			GAME_BOARD.set_el(2, 2, PLAYER)
			GAME_BOARD.del_el(self.x, self.y)	




	def interact(self, player):
		
		if len(player.inventory) == 5:
			print "beginning of if statement"
			magician = Magic()
			GAME_BOARD.register(magician)
			GAME_BOARD.set_el(GAME_WIDTH -1, GAME_HEIGHT - 3, magician)
			GAME_BOARD.draw_msg("I kind of like you, I'll let you pass.")
			GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
			GAME_BOARD.set_el(GAME_WIDTH - 5, GAME_HEIGHT - 8, PLAYER)
			GAME_BOARD.del_el(self.x, self.y)
			GAME_BOARD.draw_msg("You went through a door!")
			Wall.SOLID = False
	
			


			# self.on_key_press(symbol, modifiers)
			# WINDOW.clear()
			# joke = raw_input(">>>>>>> ")
			# if KEYBOARD[key.ENTER]:
				# GAME_BOARD.draw_msg("You said %r, I guess that's funny. You can pass") % joke			
			#	print chr(7)
				
			# else:
			# 	GAME_BOARD.draw_msg("didn't udnerstand")
		else:
			GAME_BOARD.draw_msg("Go back and find all the gems!")

		

		# global GAME_WIDTH
		# global GAME_HEIGHT
		# GAME_WIDTH = GAME_WIDTH + 5
		# GAME_HEIGHT = GAME_HEIGHT + 5

####   End class definitions    ####

def initialize():
    # """Put game initialization code here"""
	
	#creating 4 rocks on the board
	wall_positions = [
			(GAME_WIDTH - 4, GAME_HEIGHT - 10),
			(GAME_WIDTH - 4, GAME_HEIGHT - 9),
			(GAME_WIDTH - 4, GAME_HEIGHT - 8),
			(GAME_WIDTH - 3, GAME_HEIGHT - 8),
			(GAME_WIDTH - 2, GAME_HEIGHT - 8),
			(GAME_WIDTH - 1, GAME_HEIGHT - 8),
			(GAME_WIDTH - 10, GAME_HEIGHT - 9),
			(GAME_WIDTH - 10, GAME_HEIGHT - 10)

	]

	rock_positions = [
			(GAME_WIDTH - 3, GAME_HEIGHT - 7),
			(GAME_WIDTH - 3, GAME_HEIGHT - 6),
			(3,2),
			(2,3)
		]


	for pos in wall_positions:
		wall = Wall()
		GAME_BOARD.register(wall)
		GAME_BOARD.set_el(pos[0], pos[1], wall)

	rocks = []
	for pos in rock_positions:
		rock = Rock()
		GAME_BOARD.register(rock)
		GAME_BOARD.set_el(pos[0],pos[1], rock)
		rocks.append(rock)

	#last rock in the list is not solid
	# rocks[-1].SOLID = False

	for rock in rocks:
		print rock

	#creating a player on the board at position (2,2)	
	global PLAYER
	PLAYER = Character()
	GAME_BOARD.register(PLAYER)
	GAME_BOARD.set_el(2, 2, PLAYER)
	print PLAYER

	# global ROCK
	# ROCK = Rock()
	# GAME_BOARD.register(ROCK)
	# GAME_BOARD.set_el(3, 2, ROCK)
	############################
	# global MAGICIAN
	# MAGICIAN = Character()
	# IMAGE = "Cat"
	# if len(player.inventory) == 4:
	# 	GAME_BOARD.register(MAGICIAN)
	# 	GAME_BOARD.set_el(GAME_WIDTH - 7, GAME_HEIGHT - 7)

	#creating a gem on the board at (3,1)
	gem_positions = [
		(GAME_WIDTH - 2, GAME_HEIGHT - 7),
		(GAME_WIDTH - 5, GAME_HEIGHT - 2),
		(GAME_WIDTH -4, GAME_HEIGHT -6),
		(GAME_WIDTH - 7, GAME_HEIGHT - 4),
		(GAME_WIDTH - 2, GAME_HEIGHT - 9)
	]

	gems = []
	for pos in gem_positions:
		gem = Gem()
		GAME_BOARD.register(gem)
		GAME_BOARD.set_el(pos[0],pos[1], gem)
		gems.append(gem)

	gems[-1].IMAGE = "OrangeGem"
	GAME_BOARD.register(gems[-1])

	GAME_BOARD.draw_msg("This game is wicked awesome.")

	#creating a door on the board at (3,3)
	door = Door_Reset_Player()
	GAME_BOARD.register(door)
	GAME_BOARD.set_el(GAME_WIDTH-2, GAME_HEIGHT - 2, door)

	return wall_positions


def keyboard_handler():
	direction = None

	if KEYBOARD[key.UP]:
		direction = "up"
	
	elif KEYBOARD[key.DOWN]:
		direction = "down"
	
	elif KEYBOARD[key.LEFT]:
		direction = "left"
	
	elif KEYBOARD[key.RIGHT]:
		direction = "right"

	# elif KEYBOARD[key.SPACE]:
	# 	GAME_BOARD.erase_msg()
	
	# creating knowledge of next position on the board
	if direction:
		next_location = PLAYER.next_pos(direction)
		next_x = next_location[0]
		next_y = next_location[1]

		# using next position to obtain from game board the element that's there
		# in order to determine how player interacts with it
		existing_el = GAME_BOARD.get_el(next_x,next_y)
		print "existing_el is: " ,  existing_el

		if existing_el:
		# 	existing_el.interact(PLAYER)
			if existing_el.IMAGE == "Rock":
		# # 	print "blah"
		  		existing_el.interact(direction)
		  		GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
				GAME_BOARD.set_el(next_x, next_y, PLAYER)
		  	else:
		  		existing_el.interact(PLAYER)
		# 	# GAME_BOARD.del_el(ROCK.x, ROCK.y)
		# 	# GAME_BOARD.set_el(next_x, next_y, ROCK)

		if existing_el is None or not existing_el.SOLID and existing_el.IMAGE != "DoorOpen" and existing_el.IMAGE != "Rock":
			GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
			GAME_BOARD.set_el(next_x, next_y, PLAYER)

