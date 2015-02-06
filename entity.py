import math
from pyglet import gl
from pyglet.clock import schedule_once, unschedule
import pyglet
# projectile, object, geometry

class Entity:
	bolt = pyglet.resource.image("bolt.png")
	bolt.anchor_x = bolt.width // 2
	bolt.anchor_y = bolt.height // 2
	blowup = pyglet.resource.image("blowoup.png")
	blowup.anchor_x = bolt.width // 2
	blowup.anchor_y = bolt.height // 2
	
	
	def __init__(self, world, etype, x, y, **parameters):
		self.active = True
		self.world = world
		self.collidable = False
		self.blockable = False
		self.dangerous = False
		self.entitytype = etype
		
		self.texture = None
		self.vertexlist = None
		
		if etype == "geometry":
			self.collidable  = True
			self.blockable = True
			
			self.x, self.y = x, y
			self.w, self.h = parameters["dimensions"]
			
		elif etype == "projectile":
			self.dangerous = True
			self.collidable = True
			
			self.x, self.y = x, y
			
			self.speed = parameters["speed"]
			self.angle = parameters["angle"]
			
			self.sx, self.sy = math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed
			schedule_once(self.deactivate, 4.0)
			
			self.texture = pyglet.sprite.Sprite(Entity.bolt, batch=world.batch, group=world.layers[3])
	
		elif etype == "eprojectile":
			self.dangerous = False
			self.collidable = True
			
			self.x, self.y = x, y
			
			self.speed = parameters["speed"]
			self.angle = parameters["angle"]
			
			self.sx, self.sy = math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed
			schedule_once(self.deactivate, 2.0)
			self.texture = pyglet.sprite.Sprite(Entity.bolt, batch=world.batch, group=world.layers[3])
		elif etype == "smallexplosion":
			world.play("explosion")
			self.dangerous = False
			self.collidable = False
			
			self.x, self.y = x, y
			self.scale=.2
			self.rotation=0
			schedule_once(self.deactivate, .4)
			
			self.texture = pyglet.sprite.Sprite(Entity.blowup, batch=world.batch, group=world.layers[3])
			self.texture.x = self.x
			self.texture.y = self.y
			
	def deactivate(self, dt):
		if dt == -1:
			unschedule(self.deactivate)
		self.active = False
		if self.texture:
			self.texture.delete()
		
	def update(self, dt):
		if self.entitytype == "projectile" or self.entitytype == "eprojectile":
			self.x, self.y = self.x + self.sx * dt, self.y + self.sy * dt
			
			try:
				self.texture.x, self.texture.y = self.x, self.y
			except AttributeError:
				pass
		
		if self.entitytype == "smallexplosion":
			try:
				self.texture.rotation += 5 * dt
				self.texture.scale += dt * 2
			except AttributeError:
				pass
		