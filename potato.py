import pyglet
import random

class Potato:
	spacepotato = pyglet.resource.image("potato.png")
	spacepotato.anchor_x = spacepotato.width // 2
	spacepotato.anchor_y = spacepotato.height // 2
	
	def __init__(self, world):
		self.entitytype = "Potato"
		self.collidable = False
		self.dangerous = False
		self.active = True
		self.world = world
		self.x = random.randint(0, 600)
		self.y = random.randint(800, 1200)
		
		self.scale = random.random()
		
		self.speed = 300.0 * self.scale
		
		self.angle = float(random.randint(0, 360))
		
		self.texture = pyglet.sprite.Sprite(Potato.spacepotato, batch=world.batch, group=world.layers[0])
		self.texture.x = self.x
		self.texture.y = self.y
		self.texture.scale = self.scale
		self.texture.rotation = self.angle
		
	def refresh(self):
		self.x = random.randint(0, 600)
		self.y = random.randint(800, 1200)
		self.texture.x = self.x
		self.texture.y = self.y
		self.scale = random.random()
		self.angle = float(random.randint(0, 360))
		self.speed = 300.0 * self.scale
		self.texture.scale = self.scale
		self.texture.rotation = self.angle
		
	def update(self, dt):
		self.y -= self.speed * dt
		
		if self.y < 0.0:
			self.refresh()
		
		self.texture.x = self.x
		self.texture.y = self.y
		
		self.angle += self.scale
		
		self.texture.rotation = self.angle
		
	
	