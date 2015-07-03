from tile import Tile
from rect import Rect
import libtcodpy as libtcod
from object import Object

class Map:

	def __init__(self, width, height, con):
		self.MAX_ROOM_MONSTERS = 3
		self.ROOM_MIN_SIZE = 6
		self.ROOM_MAX_SIZE = 10
		self.MAX_ROOMS = 30

		self.height = height
		self.width = width
		self.objects = []
		self.con = con
		self.make_map()

	def __getitem__(self, key):
		return self.map[key]

	def make_map(self):
		self.map = [[ Tile(True)
			for y in range(self.height) ]
				for x in range(self.width) ]

		rooms = []
		num_rooms = 0

		for r in range(self.MAX_ROOMS):
			#make a random room
			w = libtcod.random_get_int(0, self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
			h = libtcod.random_get_int(0, self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)

			x = libtcod.random_get_int(0, 0, self.width - w - 1)
			y = libtcod.random_get_int(0, 0, self.height - h - 1)

			new_room = Rect(x, y, w, h)

			#make sure it doesn't intersect other rooms
			failed = False
			for other_room in rooms:
				if new_room.intersect(other_room):
					failed = True
					break

			if not failed:
				self.create_room(new_room)
				self.place_objects(new_room)
				(new_x, new_y) = new_room.center()

				if num_rooms == 0:
					self.originX = new_x
					self.originY = new_y

				else:
					#connect our room to the previous room
					(prev_x, prev_y) = rooms[num_rooms-1].center()

					if libtcod.random_get_int(0, 0, 1) == 1:
						self.create_h_tunnel(prev_x, new_x, prev_y)
						self.create_v_tunnel(prev_y, new_y, new_x)
					else:
						self.create_v_tunnel(prev_y, new_y, prev_x)
						self.create_h_tunnel(prev_x, new_x, new_y)

				rooms.append(new_room)
				num_rooms+= 1

	def place_objects(self, room):
		num_monsters = libtcod.random_get_int(0, 0, self.MAX_ROOM_MONSTERS)

		for i in range(num_monsters):
			x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
			y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

			if not self.is_blocked(x, y):
				if libtcod.random_get_int(0, 0, 100) < 80:
					monster = Object(x, y, 'o', 'Orc', libtcod.desaturated_green, self.con, True)
				else:
					monster = Object(x, y, 'T', 'Troll', libtcod.darker_green, self.con, True)

				self.objects.append(monster)

	def create_room(self, room):
		for x in range(room.x1 + 1, room.x2):
			for y in range(room.y1 + 1, room.y2):
				self.map[x][y].blocked = False
				self.map[x][y].block_sight = False

	def create_h_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2) + 1):
			self.map[x][y].blocked = False
			self.map[x][y].block_sight = False

	def create_v_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2) + 1):
			self.map[x][y].blocked = False
			self.map[x][y].block_sight = False

	def is_blocked(self, x, y):
		if self.map[x][y].blocked:
			return True

		for object in self.objects:
			if object.blocks and object.x == x and object.y == y:
				return True

		return False
